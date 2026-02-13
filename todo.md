# do-markdown Implementation Progress

## Step 1: Project Scaffolding
- [x] 1.1 Create project directory and initialize with uv
- [x] 1.2 Configure pyproject.toml (name, deps, dev deps, ruff, pytest)
- [x] 1.3 Create justfile (install, test, lint, format, check)
- [x] 1.4 Create src/do_markdown/__init__.py (kept empty per Python conventions)
- [x] 1.5 Create tests/conftest.py with shared fixtures (md_with_superfences only)
- [x] 1.6 Create tests/test_smoke.py with import and version tests
- [x] 1.7 Run uv sync and verify smoke tests pass
- [x] 1.8 Add ruff dev dependency (included in initial pyproject.toml)
- [x] 1.9 Run ruff check, verify no lint errors
- [x] 1.10 Add mypy to dev dependencies, configure [tool.mypy] strict, update justfile check command

## Step 2: Highlight Extension (`<^>...<^>`)
- [x] 2.1 RED: Write tests in tests/test_highlight.py (inline, code, fenced, multi, edge cases)
- [x] 2.2 GREEN: Implement src/do_markdown/highlight.py (InlineProcessor + Postprocessor)
- [x] 2.3 Run tests, verify all pass
- [x] 2.4 REFACTOR: Review HTML escaping and code block handling
- [x] 2.5 Run full verification (just check)

## Step 3: Fence Extension — Directive Parsing & Labels
- [ ] 3.1 RED: Write tests in tests/test_fence.py (label, secondary_label, both, no directives, special chars)
- [ ] 3.2 GREEN: Implement src/do_markdown/fence.py (FencePreprocessor + FencePostprocessor + FenceExtension)
- [ ] 3.3 Run fence tests, verify all pass
- [ ] 3.4 REFACTOR: Review HTML escaping, nested fences, blank line handling
- [ ] 3.5 Run full verification (just check)

## Step 4: Fence Extension — Environment Classes
- [ ] 4.1 RED: Write environment tests (basic, allowed list, combined with label/secondary_label)
- [ ] 4.2 GREEN: Extend fence.py with ENVIRONMENT_RE, preprocessor extraction, postprocessor class injection
- [ ] 4.3 Run fence tests, verify all pass
- [ ] 4.4 REFACTOR: Sanitize environment names, handle directive ordering
- [ ] 4.5 Run full verification (just check)

## Step 5: Fence Extension — Line Prefixes
- [ ] 5.1 RED: Write prefix tests (line_numbers, command, super_user, custom_prefix, \s, combined)
- [ ] 5.2 GREEN: Extend fence.py with prefix parsing, info string cleaning, line wrapping
- [ ] 5.3 Run fence tests, verify all pass
- [ ] 5.4 RED: Write full combo integration test (line_numbers + environment + label + language)
- [ ] 5.5 GREEN: Fix any integration issues
- [ ] 5.6 REFACTOR: Extract line-wrapping helper, handle Pygments output
- [ ] 5.7 Run full verification (just check)

## Step 6: YouTube Embed
- [ ] 6.1 RED: Write tests in tests/test_youtube.py (basic, dimensions, encoding, aspect ratio)
- [ ] 6.2 GREEN: Implement src/do_markdown/_util.py (reduce_fraction only, use html.escape() directly)
- [ ] 6.3 GREEN: Implement src/do_markdown/youtube.py (YouTubePreprocessor + YouTubeExtension)
- [ ] 6.4 Run YouTube tests, verify all pass
- [ ] 6.5 REFACTOR: Verify HTML matches reference, check line matching
- [ ] 6.6 Run full verification (just check)

## Step 7: CodePen Embed
- [ ] 7.1 RED: Write tests in tests/test_codepen.py (basic, theme, height, tabs, lazy, editable, combined, script)
- [ ] 7.2 GREEN: Implement src/do_markdown/codepen.py (Preprocessor + Postprocessor for script)
- [ ] 7.3 Run CodePen tests, verify all pass
- [ ] 7.4 REFACTOR: Verify HTML matches reference, check escaping
- [ ] 7.5 Run full verification (just check)

## Step 8: Twitter & Instagram Embeds
- [ ] 8.1 RED: Write Twitter tests in tests/test_twitter.py (basic, x.com, theme, align, width clamp, script)
- [ ] 8.2 RED: Write Instagram tests in tests/test_instagram.py (basic, caption, align, width clamp, script)
- [ ] 8.3 GREEN: Implement src/do_markdown/twitter.py
- [ ] 8.4 GREEN: Implement src/do_markdown/instagram.py
- [ ] 8.5 Run Twitter + Instagram tests, verify all pass
- [ ] 8.6 REFACTOR: Look for shared patterns, extract if 3+ extensions share logic
- [ ] 8.7 Run full verification (just check)

## Step 9: Slideshow & Image Compare Embeds
- [ ] 9.1 RED: Write Slideshow tests in tests/test_slideshow.py (basic, dimensions, min images, escaping)
- [ ] 9.2 RED: Write Image Compare tests in tests/test_image_compare.py (basic, dimensions, escaping)
- [ ] 9.3 GREEN: Implement src/do_markdown/slideshow.py
- [ ] 9.4 GREEN: Implement src/do_markdown/image_compare.py
- [ ] 9.5 Run Slideshow + Image Compare tests, verify all pass
- [ ] 9.6 REFACTOR: Review all embed extensions for consistency
- [ ] 9.7 Run full verification (just check)

## Step 10: CSS Stylesheet & MkDocs Integration
- [ ] 10.1 Add do-markdown styles to website's docs/stylesheets/extra.css
- [ ] 10.2 Add do-markdown as local dependency in website's pyproject.toml, run uv sync
- [ ] 10.3 Configure all extensions in website's mkdocs.yml
- [ ] 10.4 Create test page docs/do-markdown-test.md with all features
- [ ] 10.5 Run just build on website, verify clean build
- [ ] 10.6 Run just serve, manually verify test page renders
- [ ] 10.7 Run do-markdown test suite: just check
- [ ] 10.8 Clean up test page from nav
