

import importlib.util
from pathlib import Path

# load module file named "2-lazy_paginate.py" (invalid identifier) by path
spec = importlib.util.spec_from_file_location("lazy_paginate", str(Path(__file__).with_name("2-lazy_paginate.py")))
lazy_paginate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lazy_paginate)
lazy_pagination = lazy_paginate.lazy_pagination  # expose the function

for page in lazy_pagination(100):
    for user in page:
        print(user)
