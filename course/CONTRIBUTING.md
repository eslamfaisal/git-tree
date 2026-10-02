# Contributing to the course

- **A mistake in a script or a command?** Open an issue with the *Script error* form, or send a pull request that edits
  the episode's `beats.yml`. Every command in a script was run in the demo repository; say which one is wrong and what
  it printed for you.
- **A better Arabic phrase?** Use the *Translation fix* form. Arabic scripts are reviewed by native speakers; the
  `glossary.md` fixes the terms (which words stay in English, how they are pronounced).
- **A new episode?** Use the *Episode request* form. A request must name one concept and one feature.
- **Rules for every change:** one lesson per video; no other product's name or trademark; no feature that is not
  shipped; no media outside `assets/`; conventional commits (`docs:`, `feat:`, `fix:`, `chore:`).
- Run `python3 course/tooling/validate_course.py` before opening a pull request.
