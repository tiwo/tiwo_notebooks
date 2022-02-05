from pathlib import Path

class Folder:
    """Convenient access to your project's folders

    This finds your project folder and can be used just like a `pathlib.Path`
    """

    def __init__(self, base):
       self.base = base

    def freeze(self):
        self.base = self.base.resolve()
        return self

    def __truediv__(self, other):
        return self.base / other

    def __str__(self):
        return str(self.base)

    def __repr__(self):
        classname = self.__class__.__name__
        basedir = str(self.base)
        return f"{classname}({basedir!r})"

    @classmethod
    def find(cls, start="", markerfile=".git", strict=True):
        return cls(cls._find_base(start, markerfile, strict))


    @staticmethod
    def _find_base(start, markerfile, strict):
        candidate = Path(start)

        while candidate.exists():
            if (candidate / markerfile).exists():
                return candidate

            candidate = candidate / ".."
        
        if strict:
            raise FileNotFoundError

        return Path(start)



class DatascienceFolder(Folder):
    """Shortcuts to the customary folders used in data science
    """

    _well_known = dict(
        data="data",
        raw="data/raw",
        external="data/external",
        interim="data/interim",
        processed="data/processed",
        docs="docs",
        models="models",
        notebooks="notebooks",
        references="references",
        reports="reports",
        figures="reports/figures",
        src="src",
    )

    def __getattr__(self, name):
        try:
            return self / self._well_known[name]
        except KeyError:
            raise AttributeError(name)

    @classmethod
    def find(cls, start="", markerfile=".git", strict=True):
        return cls(cls._find_base(start, markerfile, strict))