# Raw Sources

Immutable source documents. The agent reads from here, never writes.

## Adding Sources

Drop source files into the appropriate directory:
- Web articles/clippings → `articles/`
- Papers/PDFs → `papers/`
- GitHub repos → `repos/` (clone with `git clone`)
- Forum threads → `forums/`
- Documentation/API refs → `docs/`
- Images/assets → `assets/`
- Personal files → `user/`

**Source filename convention:** `YYYY-MM-DD_slug.ext`

Once added, tell your agent to "ingest <filename>" — it will read the source,
create a summary page, update the index, and cross-reference relevant pages.
