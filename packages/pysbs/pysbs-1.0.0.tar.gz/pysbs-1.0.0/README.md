```
from pysbs import SBS
sbs = SBS(open("main.sbs", "rb"))
print(sbs["test"])
sbs["test"] = "hello"
print(sbs["test"])
sbs.dump(open("main.sbs", "wb"))
```

