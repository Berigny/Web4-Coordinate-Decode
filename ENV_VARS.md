# Environment Variables — Web4-Coordinate-Decode

Auto-generated during DSS-232 pre-migration cleanup.

This app reads configuration through Streamlit `st.secrets`. Equivalent environment variables can be supplied via `.streamlit/secrets.toml` or the deployment platform's secret manager.

| Variable | Default | Source file(s) | Purpose |
|---|---|---|---|
| `API_BASE` | `https://ds-backend-new.fly.dev` | `decoder_app.py` | Default cloud backend base URL. |
| `API_BASE_LOCAL` | `http://127.0.0.1:8080` | `decoder_app.py` | Default local backend base URL. |
| `BACKEND_ADMIN_TOKEN` | *(empty)* | `decoder_app.py` | Admin token for backend requests (`x-admin-token`). |
| `FEEDBACK_ACTOR_ID` | `human:decoder` | `decoder_app.py` | Actor ID for feedback entries. |
| `FEEDBACK_ACTOR_TYPE` | `human` | `decoder_app.py` | Actor type for feedback entries. |
| `VERIFIER_PORTAL_ID` | `web4_decoder_app` | `decoder_app.py` | Verifier portal identifier. |
| `VERIFIER_IDENTITY` | `human:decoder` | `decoder_app.py` | Verifier identity fallback. |
| `PRINCIPAL_ID` | `demo-user` | `decoder_app.py` | Principal ID header (`x-principal-id`). |
| `PRINCIPAL_TYPE` | `human` | `decoder_app.py` | Principal type header (`x-principal-type`). |
| `TENANT_ID` | `demo` | `decoder_app.py` | Tenant ID header (`x-tenant-id`). |

## Notes

- This component will be rewritten as `apps/coord-demo/` in FastHTML per the monorepo contract; these secrets should be migrated to standard `os.getenv` reads at that time.
- No production API keys were found in tracked source.
