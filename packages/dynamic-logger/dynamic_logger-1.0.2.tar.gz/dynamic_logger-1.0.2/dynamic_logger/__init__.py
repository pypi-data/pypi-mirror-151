# Author: Ankit Jain <ajatkj@yahoo.co.in>
# Report any issues on GitHub <https://github.com/ajatkj> or via email
# Version: 1.0.2
"""
Custom Logging (for logging) package to log non-standard items easily and dynamically.
Provides 2 main interfaces to the users:
- Decorator "log_extras()" to log function input arguments.
- Function "set_extras(dict)" to log static values.
- Additionally, use "clear()" to clear extras.
Make sure to set-up formatter to include the extra format fields.
i.e. to log a field called "id", include %(id)s in formatter string.
Refer @log_extras decorator for more information

To use, simply 'import dynamic_logger' and set logging.setLoggerClass(dynamic_logger.Logger)
"""

__author__ = "Ankit Jain <ajatkj@yahoo.co.in>"
__status__ = "production"
__version__ = "1.0.2"
__date__ = "09 April 2022"

import logging
from functools import wraps
import re
from typing import List


class Logger(logging.Logger):
    """
    Custom Logger class overrides logging.Logger to include "extras" in the logs
    """
    def __init__(self, name, level=0, extras: dict = None):
        self.__og_fmts = []
        self.__extras = {}
        self.__default_extras = {}
        if extras is not None:
            self.__default_extras = extras
        self.__decorated_funcs = set()
        logging.Logger.__init__(self, name=name, level=level)

    def info(self, msg, *args, **kwargs):
        self.__log(logging.INFO, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.__log(logging.WARNING, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.__log(logging.ERROR, msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.__log(logging.DEBUG, msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.__log(logging.CRITICAL, msg, *args, **kwargs)

    def fatal(self, msg, *args, **kwargs):
        self.__log(logging.FATAL, msg, *args, **kwargs)

    def __log(self, level, msg, *args, **kwargs):
        # Reset _extras if caller function is not decorated
        caller = self.findCaller()[2]
        if caller not in self.__decorated_funcs:
            if self.__default_extras == {}:
                self.__extras.clear()
                self.__extras == {}
            else:
                self.__extras.update(self.__default_extras)
        else:
            self.__extras.update(self.__default_extras)
        if self.isEnabledFor(level):
            self.__switch_formatter()
            if self.__extras == {}:
                # stacklevel is set to 2 because __log is at 2nd level (program -> info () -> __log())
                # Setting to 1 which is default will return the name of logger function i.e. info, war etc.
                self._log(level, msg, args, **kwargs, stacklevel=2)
            else:
                self._log(level, msg, args, extra=self.__extras, **kwargs, stacklevel=2)
            self.__switch_formatter(switch='off')

    def log_extras(self, **kwfields):
        """
        Decorator to log additional (extras) fields.
        The fields are extracted from the decorated function definition.
        Decorator only accepts keyword arguments. The "key" should be part of the logging format string.
            ex. to log "id", pass decorator argument "id"="user.customer_id"
        - Keyword decorator arguments can have value as either positions of positional function argument of
          the decorated function or keyword argument.
          ex. log_extras(id="0") will extract 1st positional argument value.
          ex. log_extras(id="0.user_id") will extract 1st positional argument value and extract user_id from it.
          ex. log_extras(id="UserObject.user_id") will extract keyword argument UserObject and extract user_id from it.
          All above will have no impact if formatter string doesn't contain %(id)s attribute.
        - Additionally, if you want to log the "key" itself, pass it as
          ex. "id"="id=user.customer.id" or "id"="id -> user.customer_id" and it will be shown in logs as such.
          Note that the separate value is preserved in logs.
        """
        def middle_func(func):
            self.__decorated_funcs.add(func.__name__)

            @wraps(func)
            def wrapper(*args, **kwargs):
                self.__set_up_extras(kwfields=kwfields, args=args, kwargs=kwargs)
                return func(*args, **kwargs)
            return wrapper
        return middle_func

    def preserve_extras(self, func):
        self.__decorated_funcs.add(func.__name__)

        @wraps(func)
        def wrapper(*args, **kwargs):
            # self.__set_up_extras(kwfields=kwfields,args=args, kwargs=kwargs)
            return func(*args, **kwargs)
        return wrapper

    def set_extras(self, extras: dict) -> None:
        """
        Set default extras. Input is in key:value pair.
        Ex. set_extras(app="myapp"). Make sure "app" is added to formatter string as %(app)s
        """
        self.__default_extras = extras

    def clear(self, all=False) -> None:
        """
        Clear default extras.
        Additionally clear all extras (generated by decorator) in case python version doesn't support Frames
        """
        self.__default_extras.clear()
        self.__default_extras = {}
        if all:
            self.__extras.clear()
            self.__extras = {}

    def __switch_formatter(self, switch="on") -> None:
        """
        Function to update the format string dynamically based on extras values present
        Restore original format string when switch is "off"
        """
        eff_handlers = self.handlers
        if eff_handlers == []:
            eff_handlers = self.root.handlers
        if switch == 'on':
            for handler in eff_handlers:
                handler_filter_names = []
                for f in handler.filters:
                    handler_filter_names.append(f.name)
                fmt = handler.formatter._fmt
                dtfmt = handler.formatter.datefmt
                self.__og_fmts.append([fmt, dtfmt])
                fmt = self.__remove_custom_format_attributes(fmt, handler_filter_names)
                handler.setFormatter(logging.Formatter(fmt=fmt, datefmt=dtfmt))
        else:
            for i, handler in enumerate(eff_handlers):
                fmt = self.__og_fmts[i][0]
                dtfmt = self.__og_fmts[i][1]
                self.__og_fmts.remove([fmt, dtfmt])
                handler.setFormatter(logging.Formatter(fmt=fmt, datefmt=dtfmt))
            self.__og_fmts = []

    def __remove_custom_format_attributes(self, fmt, filter_names: List = []) -> str:
        """
        Match and remove custom format attributes which are not required for this logging call
        This function checks for attributes in 3 places
        - Standard attributes provided by logging package
        - Extras set-up be either @log_extras decorator or set_extras function
        - Any filter (if filter is modifying the log record).
          For this to work filter name should match the attribute name.
        """
        # Regex to match all format attributes ex. %(name)s
        regex = r"[^ :]*%\(([a-zA-Z_]+)\)[-+]*[0-9]{0,2}[sd]{1}[^ :]*"
        # Regex to dynamically match custom attributes. Replace ==attrib== with attribute name before matching
        dyregex = r"[^ :]*%\(==attrib==\)[-+]*[0-9]{0,2}[sd]{1}[^ :]*"
        # Standard format attributes. Update this list if it is updated in logging module as well.
        st = ['name', 'levelno', 'levelname', 'pathname', 'filename', 'module', "lineno", "funcName", "created",
              "asctime", "msecs", "relativeCreated", "thread", "threadName", "process", "message"]
        attribs = re.findall(regex, fmt)
        attributes_to_be_removed = set()
        # Find out attributes to be removed by looking at the standard attributes
        # list st, keys in self.__extras and names of filters
        # If the attribute is not present in all 3 places, add to remove list
        for f in attribs:
            if f not in st and f not in self.__extras and f not in filter_names:
                attributes_to_be_removed.add(f)
        # Remove the attribs found above from the formatter
        for ff in attributes_to_be_removed:
            reg = re.sub("==attrib==", ff, dyregex)
            fmt = re.sub(reg, "", fmt)
        fmt = re.sub(" +", " ", fmt)  # remove any additional spaces
        return fmt

    def __set_up_extras(self, kwfields, args, kwargs) -> None:
        """
        Extract values of kwfields from args and kwargs.
        The "key" in kwfields is used as the message format attribute i.e. it should be present
        in the log format else value will not be displayed.
        If the "value" in kwfields is of the form "key=value", extra will be set as "key=12345"
        The separate is preserved. So, "key -> value" will be set as "key -> 12345"
        If the "value" in kwfields is just value, extra will be set as "12345"
        """
        extras = {}
        for f in kwfields:
            # If value in kwfield[f] is in the form "id=value, use "id" as the tag in extras
            # Regex to search for string of type "key=value" or "key ==> value"
            tags = re.search(r"^([a-z0-9]+)([^ a-zA-Z0-9_\.]+)(.*)", kwfields[f])
            if tags is None:
                k = f
                field = kwfields[f]
                tag = None
            else:
                tag = k = tags.group(1)
                sep = tags.group(2)
                field = tags.group(3)
            ef = self.__extract_field(field, args=args, kwargs=kwargs)
            if ef is not None:
                if tag:
                    extras[k] = f"{tag}{sep}{ef}"
                else:
                    extras[k] = f"{ef}"
        if extras:
            self.__extras = extras
        else:
            self.__extras = {}

    def __extract_field(self, field: str, args, kwargs) -> str:
        """
        Extract field from *args & **kwargs. Following happens:
        - If field contains a "." or "[", it is split with "." and "["
        - If the result is a single item then the value of it is returned based on
            + If it is a number, then it represents positional argument and respective value is returned if present
                e.g. 0
            + If it is a string, then it represents keyword argument. Respective keyword value is extracted if present
                e.g. customer_id
        - If the result is more than 1 item, the whole expression is evaluated to return its value
                e.g. user['customer_id'] or user.customer_id
        - The function doesn't throw any error. If a field is not present, it is simply ignored
        """
        fields = re.split(r"[.\[]", str(field))
        if len(fields) == 1:  # not a dictionary, just return the value from args or kwargs
            if str(field).isnumeric():
                return args[field] if int(field) < len(args) else None
            return kwargs.get(field) if kwargs.get(field) else None
        # Check if first part of list is a numeric value
        if str(fields[0]).isnumeric():
            basefield = args[int(fields[0])] if int(fields[0]) < len(args) else None
        else:
            # At this point, the field is an Object
            basefield = kwargs.get(fields[0], None)
        if basefield is None:
            return None
        eval_field = re.sub(fields[0], 'basefield', field, count=1)
        try:
            value = eval(eval_field)
        except Exception:
            return None
        return value
