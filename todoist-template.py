import sys
import logging
import argparse
import lib.key_ring as keyring
from lib.template import TodoistTemplate

class StoreDictKeyPair(argparse.Action):
	def __call__(self, parser, namespace, values, option_string=None):
		my_dict = {}
		for kv in values.split(","):
			k,v = kv.split("=")
			my_dict[k] = v
		setattr(namespace, self.dest, my_dict)

def parse_cmd_line():
	parser = argparse.ArgumentParser(prog="todoist-template.py", usage='%(prog)s [options]', description='Creates Todoist tasks from a YAML template')

	# positional arguments:
	parser.add_argument(
		'template',
		type=argparse.FileType('r', encoding="utf8"))

	# options
	parser.add_argument("-D",
		dest="placeholders",
		action=StoreDictKeyPair,
		metavar="KEY0=VAL0,KEY1=VAL1...",
		help='the placeholder values replaced in template')

	parser.add_argument('--version',
		action='version',
		version='%(prog)s 1.0.0')

	parser.add_argument('--id',
		dest='service_id',
		default="TODOIST-TEMPLATE",
		help='keyring service name where store Todoist API Token')

	command_group = parser.add_mutually_exclusive_group()
	command_group.add_argument('-d', '--debug',
		dest='loglevel',
		default=logging.INFO, action='store_const', const=logging.DEBUG,
		help='more verbose output')
	command_group.add_argument('-q', '--quiet',
		dest='loglevel',
		default=logging.INFO, action='store_const', const=logging.NOTSET,
		help='suppress output')

	return parser.parse_args()

def main():
	args = parse_cmd_line()
	logging.basicConfig(level=args.loglevel, format="[%(levelname)s] %(message)s")

	try:
		api_token = keyring.get_api_token(args.service_id)
		while not api_token:
			logging.warning(f"Todoist API token not found for {args.service_id} application.")
			keyring.setup(args.service_id)
			api_token = keyring.get_api_token(args.service_id)

		tmpl = TodoistTemplate(api_token)
		with args.template as file:
			logging.debug(f"open file {file}")
			tmpl.parse(file, args.placeholders)

		return 0
	except Exception as e:
		logging.error(e, exc_info=True)
		return 1

if __name__ == "__main__":
	sys.exit(main())