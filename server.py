from core import mcp
from tools import (  # noqa: F401  (imports register the tools)
    contacts,
    directory,
    tickets,
)

if __name__ == "__main__":
    mcp.run(transport="stdio")
