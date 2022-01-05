import fnmatch
import re
import os
import mkdocs
import mkdocs.plugins
import mkdocs.structure.files


class Include(mkdocs.plugins.BasePlugin):
    """A mkdocs plugin that adds all matching files from the input list."""

    config_scheme = (
        ('ext', mkdocs.config.config_options.Type((str, list), default=[
            ".md", ".markdown", ".mdown", ".mkdn", ".mkd", ".css",
            ".js", ".javascript", ".html", ".htm", ".xml", ".json",
            ".bmp", ".tif", ".tiff", ".gif", ".svg", ".jpeg",
            ".jpg", ".jif", ".jfif", ".jp2", ".jpx", ".j2k",
            ".j2c", ".fpx", ".pcd", ".png", ".pdf", "CNAME",
            ".snippet", ".pages"
        ])),
        ('glob', mkdocs.config.config_options.Type((str, list), default=None)),
        ('regex', mkdocs.config.config_options.Type((str, list), default=None)),
    )

    def on_files(self, files, config):
        exts = self.config['ext'] or []
        if not isinstance(exts, list):
            exts = [exts]
        globs = self.config['glob'] or []
        if not isinstance(globs, list):
            globs = [globs]
        regexes = self.config['regex'] or []
        if not isinstance(regexes, list):
            regexes = [regexes]
        out = []

        def include(name):
            if os.path.splitext(name)[1] in exts:
                return True
            for g in globs:
                if fnmatch.fnmatchcase(name, g):
                    return True
            for r in regexes:
                if re.match(r, name):
                    return True
            return False

        for i in files:
            name = i.src_path
            if not include(name):
                continue

            # Windows reports filenames as eg.  a\\b\\c instead of a/b/c.
            # To make the same globs/regexes match filenames on Windows and
            # other OSes, let's try matching against converted filenames.
            # On the other hand, Unix actually allows filenames to contain
            # literal \\ characters (although it is rare), so we won't
            # always convert them.  We only convert if os.sep reports
            # something unusual.  Conversely, some future mkdocs might
            # report Windows filenames using / separators regardless of
            # os.sep, so we *always* test with / above.
            if os.sep != '/':
                namefix = name.replace(os.sep, '/')
                if not include(namefix):
                    continue
            out.append(i)
        return mkdocs.structure.files.Files(out)
