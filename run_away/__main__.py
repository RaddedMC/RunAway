import sys

from run_away.main import main

rc = 1
try:
    main()
    rc = 0
except Exception as ex:
    print(f"Error: {ex}", file=sys.stderr)
sys.exit(rc)
