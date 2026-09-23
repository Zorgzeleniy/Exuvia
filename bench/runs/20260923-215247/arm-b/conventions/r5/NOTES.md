# Project Notes

## Organization

- Standing conventions are defined by the corpus: `conventions.json` (commit
  format and markdown file rules) and `qa.json` (documentation checklist).
- Documentation lives in markdown; internal references use relative paths.
- Commits follow `type(scope): subject` — `type` is one of `feat`, `fix`,
  `docs`, `chore`, `refactor`, `test`, and `scope` is `[a-zA-Z0-9_-]+`.

## Quality gate

- Commit messages are validated against:

```regex
^(feat|fix|docs|chore|refactor|test)\([a-zA-Z0-9_-]+\): \S.+
```

- Markdown files must end with a newline, contain no trailing whitespace, and
  every code fence must declare a language.
- Never commit or push without an explicit request, and never add a
  `Co-Authored-By: Claude` trailer.
