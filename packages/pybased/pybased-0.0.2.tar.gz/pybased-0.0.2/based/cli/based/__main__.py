
from base64 import b64encode
import hashlib
import json
from typing import BinaryIO, Dict, List, Optional, TextIO
import click
import tabulate
import argparse
import sys
from based.abcs import IBaseConverter
from based.converters.bigint import BigIntBaseConverter
from based.converters.biterator import BiteratorBaseConverter
from based.converters.slidingwindow import SlidingWindowBaseConverter
from based.standards import ALL

def main():
    argp = argparse.ArgumentParser()
    subp = argp.add_subparsers()

    _register_dump(subp)
    _register_encode(subp)
    _register_decode(subp)

    args = argp.parse_args()
    if hasattr(args, 'cmd'):
        args.cmd(args)
    else:
        argp.print_usage()

def _register_dump(subp: argparse._SubParsersAction) -> None:
    p: argparse.ArgumentParser = subp.add_parser('dump')
    p.add_argument('--format', choices=[f for f in tabulate.tabulate_formats]+['readme.md'], default='github')
    p.set_defaults(cmd=_cmd_dump)


def _cmd_dump(args: argparse.Namespace) -> None:
    import tabulate
    try:
        from html import escape as html_escape  # python 3.x
    except ImportError:
        from cgi import escape as html_escape  # python 2.x
    entries = []
    header = ['ID', 'Type', 'Bits/Char', 'Chars/Byte', 'Alphabet']
    def _b(instr: str) -> str:
        if args.format in ('html','markdown'):
            return f'<strong>{instr}</strong>'
        return instr
    def _code(instr: str) -> str:
        if args.format in ('html', 'markdown'):
            p = html_escape(instr)
            p=p.replace('\\', '\\\\')
            p=p.replace('|', '\|')
            return f'<strong>{p}</code>'
        return instr
    for base in sorted(ALL, key=lambda x: x.id):
        if isinstance(base, SlidingWindowBaseConverter):
            entries += [[_b(base.id), base.CONVERTER_TYPE_NAME, base.bits_per_char, base.chars_per_byte, _code(base.alphabet)]]
        if isinstance(base, BiteratorBaseConverter):
            entries += [[_b(base.id), base.CONVERTER_TYPE_NAME, base.bits_per_char, base.pad_modulo, _code(base.alphabet)]]
        elif isinstance(base, BigIntBaseConverter):
            entries += [[_b(base.id), base.CONVERTER_TYPE_NAME, 'N/A', 'N/A', _code(base.alphabet)]]
    if args.format in ('html', 'readme.md', 'markdown'):
        html = '<table><thead><caption>Supported Encodings</caption><tr>'
        html += ''.join([f'<th>{c}</th>' for c in header])
        html += '</tr></thead><tbody>'
        for row in entries:
            html += '<tr>'
            html += f'<th>{row[0]}</th>'
            html += f'<td>{row[1]}</td>'
            html += f'<td>{row[2]}</td>'
            html += f'<td>{row[3]}</td>'
            html += f'<td><code>{html_escape(row[4])}</code></td>'
            html += '</tr>'
        html += '</tbody></table>'
        print(html)
    else:
        print(tabulate.tabulate(entries, headers=header, tablefmt=args.format if args.format != 'readme.md' else 'html'))

def _register_decode(subp: argparse._SubParsersAction) -> None:
    p: argparse.ArgumentParser = subp.add_parser('decode')
    p.add_argument('--standard', '-s', choices=[x.id for x in ALL], nargs='?', help='Which standard to decode from.')
    ip = p.add_mutually_exclusive_group()
    ip.add_argument('--input-file', '-F', type=argparse.FileType('rb'), default=None, help='Use an input file rather than a string input')
    ip.add_argument('--input-string', type=str, default=None)
    p.add_argument('--input-string-encoding', '-i', type=str, default='utf-8', help='Encoding of the input string.')
    p.add_argument('--output-file', '-O', type=argparse.FileType('wb'), default=None, help='Use an output file rather than stdout')
    p.add_argument('--output-format', '-o', choices=['raw', 'python', 'json', 'yaml'], default='raw', help='How to format the output.')
    p.set_defaults(cmd=_cmd_decode)
    
def _cmd_decode(args: argparse.Namespace) -> None:
    o = []
    origstr: str = ''
    if args.input_file is None:
        origstr = args.input_string
    else:
        origstr = args.input_file.read().decode(args.input_string_encoding)
    lenorigb = len(origstr)
    click.secho(f'>>> input chars: {lenorigb}B', fg='cyan')
    out: Optional[BinaryIO] = args.output_file
    conv: IBaseConverter = next(c for c in ALL if c.id == args.standard)
    o: bytes = conv.decode_bytes(origstr)
    if args.output_format == 'raw' and out is None:
        click.echo(f'Bytes representation: {o!r}')
        click.echo(f'Hex representation: {o.hex()}')
        return
    if args.output_format == 'raw':
        pass
    elif args.output_format == 'python':
        o = repr(o).encode('utf-8')
    elif args.output_format == 'json':
        jsondata: Dict[str, str] = {
            'b64': b64encode(o).decode('ascii')
        }
        try:
            jsondata['utf-8'] = o.decode('utf-8')
        except UnicodeDecodeError:
            pass
        o = json.dumps(jsondata).encode('utf-8')
    elif args.output_format == 'yaml':
        from ruamel.yaml import YAML
        yaml = YAML(typ='rt', pure=True)
        yaml.dump({'encoded':o}, out or sys.stdout)
        return
    if out is None:
        print(o.decode('utf-8'))
    else:
        out.write(o)

def _register_encode(subp: argparse._SubParsersAction) -> None:
    p: argparse.ArgumentParser = subp.add_parser('encode')
    p.add_argument('--standard', '-s', choices=[x.id for x in ALL], nargs='?', default=None, help='Which standard to encode to. default=Try on all standards and output to table')
    ip = p.add_mutually_exclusive_group()
    ip.add_argument('--input-file', '-F', type=argparse.FileType('rb'), default=None, help='Use an input file rather than a string input')
    ip.add_argument('--input-string', type=str, default=None)
    p.add_argument('--input-string-encoding', '-i', type=str, default='utf-8', help='Encoding of the input string.')
    p.add_argument('--output-file', '-O', type=argparse.FileType('w'), default=None, help='Use an output file rather than stdout')
    p.add_argument('--output-format', '-o', choices=['ascii', 'json', 'yaml', 'readme.md'], default='ascii', help='How to format the output.')
    p.add_argument('--verbose', '-v', action='count', default=0, help='Additional verbosity')
    p.set_defaults(cmd=_cmd_encode)
    
def _cmd_encode(args: argparse.Namespace) -> None:
    import tabulate
    try:
        from html import escape as html_escape  # python 3.x
    except ImportError:
        from cgi import escape as html_escape  # python 2.x
    o = []
    origb: bytes = b''
    if args.input_file is None:
        origb = args.input_string.encode(args.input_string_encoding)
        if args.verbose > 1: 
            click.secho(f'>>> input as hex:   {origb.hex()}', fg='cyan')
            click.secho(f'>>> input as bytes: {origb!r}', fg='cyan')
    else:
        origb = args.input_file.read()
    lenorigb = len(origb)
    if args.verbose > 1:
        click.secho(f'>>> input bytes: {lenorigb}B', fg='cyan')
    out: TextIO = args.output_file or sys.stdout
    if args.standard is None:
        hdr = ['Standard', 'Encoded', 'Decoded', 'Passed Test']
        def _b(instr: str) -> str:
            if args.output_format in ('html', 'markdown'):
                return f'<strong>{instr}</strong>'
            return instr
        def _bool2chk(val: bool) -> str:
            if args.output_format in ('html', 'markdown', 'readme.md'):
                return '✔' if val else '❌'
            return 'Yes' if val else 'No'
        def _code(instr: str) -> str:
            if isinstance(instr, bytes):
                instr = repr(instr)
            if args.output_format in ('html', 'markdown', 'readme.md'):
                p = html_escape(instr)
                p = p.replace('\\', '\\\\')
                p = p.replace('|', '\|')
                return f'<code>{p}</code>'
            return instr
        errs=[]
        for base in sorted(ALL, key=lambda x: x.id):
            row = [_b(base.id), 'ERR', 'ERR', '❌']
            try:
                enc: str = base.encode_bytes(origb)
                decb: str = base.decode_bytes(enc)
                row: List[str]
                #assert lenorigb == len(decb), f'lenorigb={lenorigb}, len(decb)={len(decb)}'
                dec: str = decb.decode('utf-8')
                row = [_b(base.id), _code(enc), _code(decb), _bool2chk(decb == origb)]
            except Exception as e:
                errs.append(e)
            o.append(row)
        if args.output_format in ('html', 'readme.md', 'markdown'):
            html = '<table><thead><caption>Supported Encodings</caption><tr>'
            html += ''.join([f'<th>{c}</th>' for c in hdr])
            html += '</tr></thead><tbody>'
            for row in o:
                html += '<tr>'
                html += f'<th>{row[0]}</th>'
                html += f'<td>{row[1]}</td>'
                html += f'<td>{row[2]}</td>'
                html += f'<td>{row[3]}</td>'
                html += '</tr>'
            html += '</tbody></table>'
            if len(errs):
                html += '<strong>Errors:</strong>'
                for e in errs:
                    html += f'<pre>{html_escape(str(e))}</pre>'
            print(html)
        else:
            click.echo(tabulate.tabulate(o, headers=hdr), file=out)
            if len(errs):
                click.secho(f'Errors:', fg='red', err=True)
                for e in errs:
                    click.secho(e, fg='red', err=True)
    else:
        conv: IBaseConverter = next(c for c in ALL if c.id == args.standard)
        o: str = conv.encode_bytes(origb)
        if args.output_format == 'ascii':
            pass
        elif args.output_format == 'json':
            o = json.dumps({'encoded':o})
        elif args.output_format == 'yaml':
            from ruamel.yaml import YAML
            yaml = YAML(typ='rt', pure=True)
            yaml.dump({'encoded':o}, out)
            out.write('\n')
            return
        out.writelines([o])
        out.write('\n')
        
if __name__ == "__main__":
    main()