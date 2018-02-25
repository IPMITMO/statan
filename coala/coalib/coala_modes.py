def mode_normal(console_printer, log_printer, args, debug=False):
    """
    This is the default coala mode. User interaction is allowed in this mode.

    :param console_printer: Object to print messages on the console.
    :param log_printer:     Deprecated.
    :param args:            Alternative pre-parsed CLI arguments.
    :param debug:           Run in debug mode, bypassing multiprocessing,
                            and not catching any exceptions.
    """
    import functools

    from coalib.coala_main import run_coala
    from coalib.output.ConsoleInteraction import (
        acquire_settings, nothing_done,
        print_results, print_section_beginning)

    partial_print_sec_beg = functools.partial(
        print_section_beginning,
        console_printer)
    results, exitcode, _ = run_coala(
        print_results=print_results,
        acquire_settings=acquire_settings,
        print_section_beginning=partial_print_sec_beg,
        nothing_done=nothing_done,
        console_printer=console_printer,
        args=args,
        debug=debug)

    return exitcode


def mode_non_interactive(console_printer, args, debug=False):
    import functools

    from coalib.coala_main import run_coala
    from coalib.output.ConsoleInteraction import (
        print_results_no_input, print_section_beginning)

    partial_print_sec_beg = functools.partial(
        print_section_beginning,
        console_printer)
    results, exitcode, _ = run_coala(
        print_results=print_results_no_input,
        print_section_beginning=partial_print_sec_beg,
        force_show_patch=True,
        console_printer=console_printer,
        args=args,
        debug=debug)

    return exitcode


def mode_json(args, debug=False):
    import json

    from coalib.coala_main import run_coala
    from coalib.output.Logging import configure_json_logging
    from coalib.output.JSONEncoder import create_json_encoder

    if args.log_json:
        log_stream = configure_json_logging()

    JSONEncoder = create_json_encoder(use_relpath=args.relpath)

    results, exitcode, _ = run_coala(args=args, debug=debug)

    retval = {'results': results}

    if args.log_json:
        retval['logs'] = [json.loads(line) for line in
                          log_stream.getvalue().splitlines()]

    if args.output:
        filename = str(args.output[0])
        with open(filename, 'w') as fp:
            json.dump(retval, fp,
                      cls=JSONEncoder,
                      sort_keys=True,
                      indent=2,
                      separators=(',', ': '))
    else:
        print(json.dumps(retval,
                         cls=JSONEncoder,
                         sort_keys=True,
                         indent=2,
                         separators=(',', ': ')))

    return 0 if args.show_bears else exitcode


def mode_format(args, debug=False):
    from coalib.coala_main import run_coala
    from coalib.output.ConsoleInteraction import print_results_formatted

    _, exitcode, _ = run_coala(
            print_results=print_results_formatted, args=args, debug=debug)
    return exitcode

def mode_statan(args, debug=False):
    import json
    import sys

    from coalib.coala_main import run_coala
    from coalib.output.Logging import configure_json_logging
    from coalib.output.JSONEncoder import create_json_encoder
    from coalib.results.AnalyzerResult import AnalyzerResult
    from coalib.settings.ConfigurationGathering import load_configuration

    from coalib.output.database import StoreException, AnalyzerResultStore

    JSONEncoder = create_json_encoder(use_relpath=args.relpath)

    results, exitcode, _ = run_coala(args=args, debug=debug)

    arg_parser=None
    arg_list = []
    if args is None:
        # Note: arg_list can also be []. Hence we cannot use
        # `arg_list = arg_list or default_list`
        arg_list = sys.argv[1:] if arg_list is None else arg_list
    sections, targets = load_configuration(arg_list, arg_parser=arg_parser,
                                           args=args)
    lan = sections['cli'].get('language', '')
    lan_v = sections['cli'].get('language_version', '')
    prj = sections['cli'].get('project', '')
    prj_v = sections['cli'].get('project_version', '')
    params = sections['cli'].get('params', '')

    messages = results['cli']
    analyzer_results = []
    for message in messages:
        dif = json.dumps(message.diffs,
                         cls=JSONEncoder,
                         sort_keys=True,
                         indent=2,
                         separators=(',', ': '))
        ''' analyzer_results.append(AnalyzerResult(message.origin,
            lan.value,
            lan_v.value,
            prj.value,
            prj_v.value,
            message.affected_code[0].file,
            message.message,
            message.severity,
            dif,
            message.confidence)) '''

        try:
            with AnalyzerResultStore() as result_store:
                result_store.addResult(AnalyzerResult(message.origin,
                    lan.value,
                    lan_v.value,
                    prj.value,
                    prj_v.value,
                    message.affected_code[0].file,
                    message.message,
                    params.value,
                    message.affected_code[0].start.line,
                    message.severity,
                    dif,
                    message.confidence))
                result_store.complete()
        except StoreException as e:
            print(e)

    ''' retval = {'results': results}

    if args.output:
        filename = str(args.output[0])
        with open(filename, 'w') as fp:
            json.dump(retval, fp,
                      cls=JSONEncoder,
                      sort_keys=True,
                      indent=2,
                      separators=(',', ': '))
    else:
        print(json.dumps(retval,
                         cls=JSONEncoder,
                         sort_keys=True,
                         indent=2,
                         separators=(',', ': '))) '''

    return 0 if args.show_bears else exitcode
