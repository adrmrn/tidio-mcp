# Tidio MCP Server

A Model Context Protocol (MCP) server that integrates with the Tidio customer service platform.  

It acts as a layer over the [Tidio OpenAPI (REST API)](https://developers.tidio.com/reference), making Tidio functionality available directly in LLM clients such as Claude Desktop.

## Requirements

- **Tidio Account** — Tidio Plus plan (or higher)  
- **API Credentials** — Client ID and Client Secret (see the [authorization guide](https://developers.tidio.com/docs/openapi-authorization))  
- **Environment** — Docker, or Python 3.13+ with [uv](https://github.com/astral-sh/uv)

## Setup

### Option 1: Non-Technical Users (Claude Desktop + Docker)

You can quickly get started using the ready-to-use Docker image `adrmrn/tidio-mcp` from [Docker Hub](https://hub.docker.com/r/adrmrn/tidio-mcp).

1. Install and run [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. Install and open [Claude Desktop](https://claude.ai/download)
3. In Claude Desktop, go to **Settings** → **Developer** → **Edit Config**, and open the `claude_desktop_config.json` file in a text editor
4. Add the following configuration, replacing the placeholders with your Tidio credentials:

   ```json
   {
     "mcpServers": {
       "Tidio": {
         "command": "docker",
         "args": [
           "run", "-i", "--rm",
           "-e", "TIDIO_CLIENT_ID",
           "-e", "TIDIO_CLIENT_SECRET",
           "adrmrn/tidio-mcp:latest"
         ],
         "env": {
           "TIDIO_CLIENT_ID": "PASTE_YOUR_CLIENT_ID_HERE",
           "TIDIO_CLIENT_SECRET": "PASTE_YOUR_CLIENT_SECRET_HERE"
         }
       }
     }
   }
   ```

5. Save the file and restart Claude Desktop

### Option 2: Technical Users (Python)

1. Clone this repository
2. Install dependencies with `uv sync`
3. Copy `.env.example` to `.env` and set your Tidio credentials
4. Add the following configuration to your MCP client:

   ```json
   {
     "mcpServers": {
       "Tidio": {
         "command": "uv",
         "args": [
           "--directory",
           "/absolute/path/tidio-mcp",
           "run",
           "server.py"
         ]
       }
     }
   }
   ```

5. Restart your MCP client to apply the configuration  

## Available Tools

- Get Departments
- Get Operators
- Get Contacts
- Get Contact Details
- Delete Contact
- Get Tickets
- Get Ticket Details
- Create Ticket
- Update Ticket
- Delete Ticket
- Unassign Ticket
- Reply to Ticket
- Add Internal Note to Ticket

## Planned Features / Missing Endpoints

- [ ] Pagination
- [ ] Filtering

The following endpoints are not yet implemented but are planned for future updates:

- [ ] Create contact (`POST /contacts`)
- [ ] Create multiple contacts (`POST /contacts/batch`)
- [ ] Update multiple contacts (`PATCH /contacts/batch`)
- [ ] Update contact properties (`PATCH /contacts/{contact_id}`)
- [ ] Get viewed pages history (`GET /contacts/{contact_id}/viewed-pages`)
- [ ] Get contact properties (`GET /contact-properties`)
- [ ] Get contact messages (`POST /contacts/{contact_id}/messages`)
- [ ] Upsert products (`PUT /products/batch`)
- [ ] Delete product (`DELETE /products/{product_id}`)

## Contributing

Contributions are welcome!  
If you’d like to improve this project, feel free to open an issue or submit a PR.

For development, the repository includes a `Makefile` with handy commands to build, debug, and test the project.
