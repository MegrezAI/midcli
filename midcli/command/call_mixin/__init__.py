# -*- coding=utf-8 -*-
import copy
import logging
import traceback

from middlewared.client import ClientException, ValidationErrors

from midcli.command.interface import ProcessInputError
from midcli.middleware import format_error, format_validation_errors
from midcli.pager import echo_via_pager

logger = logging.getLogger(__name__)

__all__ = ["CallMixin"]


class CallMixin(object):
    output_processors = []

    def __init__(self, *args, **kwargs):
        self.job_last_printed_description = ""
        self.output = kwargs.pop("output", True)

        super().__init__(*args, **kwargs)

    def _process_call_args(self, args):
        """
        Transforms args before passing them to the middleware (e.g. rename poorly named arguments)
        """
        return args

    def call(self, name, *args, job=False, output_processor=None, raise_=False):
        try:
            args = self._process_call_args(copy.deepcopy(args))

            with self.context.get_client() as c:
                rv = c.call(name, *args, job=job, callback=self._job_callback)

            for op in self.output_processors:
                rv = op(self.context, rv)

            if output_processor is not None:
                rv = output_processor(rv)
        except Exception as e:
            if raise_:
                raise

            if (error := self._handle_error(e)) is not None:
                raise ProcessInputError(error)
            else:
                raise ProcessInputError(traceback.format_exc())
        else:
            self._handle_output(rv)

            return rv

    def _call_util(self, method, *args, **kwargs):
        with self.context.get_client() as c:
            try:
                return c.call(method, *args, **kwargs)
            except Exception as e:
                if (error := self._handle_error(e)) is not None:
                    raise ProcessInputError(f"Error while calling {method}(*{args!r}, **{kwargs!r}):\n{error}")

                raise

    def _handle_error(self, e):
        if isinstance(e, ValidationErrors):
            return (
                "Validation errors:\n" +
                format_validation_errors(e) +
                ("\nHint: Add -- to the end of the command to open an interactive arguments editor"
                 if any(error.errmsg == "attribute required" for error in e.errors) else "")
            )

        if isinstance(e, ClientException):
            return format_error(self.context, e)

        return None

    def _handle_output(self, rv):
        if self.output:
            echo_via_pager(self.context.display_mode_manager.mode.display(rv))

    def _job_callback(self, job):
        text = f"[{int(job['progress']['percent'] or 0)}%] {job['progress']['description']}..."

        if text != self.job_last_printed_description:
            print(text)

        self.job_last_printed_description = text
