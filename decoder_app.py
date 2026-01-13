import streamlit as st
import requests
import time
import graphviz
from typing import List, Literal, TypedDict, Union

# --- TYPES ---
class Meta(TypedDict, total=False):
    namespace: str
    type: str
    coherence: Union[float, str]
    mediator: str
    timestamp: str
    raw: dict


class Content(TypedDict, total=False):
    summary: str
    claims: List[str]
    context: str
    raw: dict


class DecodeResultSuccess(TypedDict, total=False):
    status: Literal["success"]
    meta: Meta
    primes: List[int]
    content: Content
    raw: dict


class DecodeResultError(TypedDict):
    status: Literal["error"]
    detail: str


DecodeResult = Union[DecodeResultSuccess, DecodeResultError]

# --- CONFIGURATION ---
API_BASE = "https://dualsubstrate-commercial.fly.dev"

st.set_page_config(
    page_title="Web4 Universal Resolver",
    page_icon="078079",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- STYLING ---
st.markdown("""
<style>
    .reportview-container { background: #fafafa; }
    h1 { font-family: 'Times New Roman', serif; font-weight: 400; color: #111; }
    .stTextInput input { font-family: 'Courier New', monospace; border-bottom: 2px solid #333; }
    .success-box {
        padding: 20px;
        border-left: 4px solid #10b981;
        background-color: #f0fdf4;
        font-family: 'Helvetica', sans-serif;
    }
    .metric-label { font-size: 0.8rem; text-transform: uppercase; color: #666; }
</style>
""", unsafe_allow_html=True)

st.title("DualSubstrate // Resolver")

# --- HELPER FUNCTIONS ---

def normalize_success(payload: dict, coord_hint: str) -> DecodeResultSuccess:
    """Normalize backend payloads into a consistent shape."""
    meta_source = payload.get("meta") or payload.get("metadata") or {}
    namespace_hint = payload.get("namespace_used") or payload.get("namespace")

    normalized_meta: Meta = {
        "namespace": namespace_hint
            or meta_source.get("namespace")
            or (coord_hint.split(":")[0] if ":" in coord_hint else coord_hint),
        "type": meta_source.get("type") or meta_source.get("kind") or payload.get("kind") or "unknown",
        "coherence": meta_source.get("coherence")
            or meta_source.get("score")
            or meta_source.get("appraisal", {}).get("score", "N/A"),
        "mediator": meta_source.get("mediator") or meta_source.get("provider") or payload.get("provider", "N/A"),
        "timestamp": meta_source.get("timestamp")
            or payload.get("created_at")
            or meta_source.get("session_id", "N/A"),
        "raw": meta_source or payload,
    }

    content_payload = payload.get("content") or {}
    if not content_payload:
        content_payload = {
            "summary": payload.get("assistant_reply") or payload.get("full_text") or "No summary provided.",
            "claims": payload.get("knowledge_tree") or [],
            "context": payload.get("user_message") or coord_hint,
        }

    normalized_content: Content = {
        "summary": content_payload.get("summary", "No summary provided."),
        "claims": content_payload.get("claims", []) or content_payload.get("knowledge_tree", []),
        "context": content_payload.get("context", payload.get("coordinate", "")),
        "raw": content_payload
    }

    return {
        "status": "success",
        "meta": normalized_meta,
        "primes": payload.get("primes") or payload.get("token_primes") or [],
        "content": normalized_content,
        "raw": payload
    }


def decode_coordinate(coord: str, silent: bool = False) -> DecodeResult:
    """Calls the backend to resolve the coordinate."""
    try:
        if not silent:
            with st.status("Establishing Coherence Handshake...", expanded=True) as status:
                st.write("078095 Parsing Namespace Prefix...")
                time.sleep(0.2)
                st.write("07806e Verifying Ledger Integrity...")

                response = requests.post(
                    f"{API_BASE}/web4/decode",
                    json={"coordinate": coord},
                    headers={"Content-Type": "application/json"}
                )
                status.update(label="Handshake Verified", state="complete")
        else:
            response = requests.post(
                f"{API_BASE}/web4/decode",
                json={"coordinate": coord},
                headers={"Content-Type": "application/json"}
            )

        body = response.json()
        payload = body.get("data") or body.get("result") or body

        if response.ok and (body.get("status") == "success" or "coordinate" in payload):
            return normalize_success(payload, coord)

        detail = payload.get("detail") or payload.get("error") or response.text
        return {"status": "error", "detail": detail}

    except Exception as e:
        return {"status": "error", "detail": str(e)}

# --- TABS LAYOUT ---

tab_resolve, tab_walk = st.tabs(["Resolve COORD", "COORD Walk Simulator"])

# ==========================================
# TAB 1: RESOLVE COORD
# ==========================================
with tab_resolve:
    st.markdown("### Universal Coherence Decoder")
    st.markdown("""
    This tool demonstrates **Protocol Independence**. 
    By inputting a Web4 Coordinate, any system with Ledger access can reconstruct the knowledge tree without a central platform.
    """)

    st.divider()

    coordinate_input = st.text_input(
        "Enter Web4 Coordinate",
        placeholder="e.g. EV-Demo-Session-123",
        help="Paste a Coordinate ID (EV, WX, ATT, etc)."
    )

    if st.button("Resolve Coordinate", type="primary", key="btn_resolve"):
        if not coordinate_input:
            st.error("Please enter a coordinate.")
        else:
            result = decode_coordinate(coordinate_input)

            if result.get("status") == "success":
                meta = result.get("meta") or {}
                content = result.get("content") or {}

                c1, c2, c3 = st.columns(3)
                c1.metric("Coherence Norm", f"{meta.get('coherence', 'N/A')}")
                c2.metric("Mediator Prime", meta.get('mediator', 'N/A'))
                c3.metric("Type", meta.get('type', 'N/A'))

                st.divider()

                st.subheader("Reconstructed Knowledge Tree")
                st.markdown(f"""
                <div class="success-box">
                    <b>Summary:</b> {content.get('summary', 'No summary provided.')}
                </div>
                """, unsafe_allow_html=True)

                st.markdown("#### Key Claims (Prime Nodes)")
                claims = content.get('claims') or []
                if claims:
                    for claim in claims:
                        st.markdown(f"- 078078 *{claim}*")
                else:
                    st.caption("No discrete prime nodes returned.")

                with st.expander("View Raw Ledger JSON"):
                    st.json(result.get("raw"))
            else:
                st.error(f"Resolution Failed: {result.get('detail')}")

# ==========================================
# TAB 2: COORD WALK SIMULATOR
# ==========================================
with tab_walk:
    st.markdown("### Ecosystem Walk Simulator")
    st.markdown("""
    This module simulates the **Inference Engine** traversing the knowledge graph.
    It hops from a starting coordinate to related memories based on coherence scores.
    """)

    c_start, c_hops = st.columns([3, 1])
    with c_start:
        start_coord = st.text_input("Start Coordinate", placeholder="e.g. EV-882", key="walk_start")
    with c_hops:
        hop_count = st.number_input("Hops", min_value=1, max_value=10, value=5, key="walk_hops")

    if st.button("Simulate Walk", type="primary", key="btn_walk"):
        if not start_coord:
            st.error("Start coordinate required.")
        else:
            with st.spinner("Calculating optimal traversal path..."):
                try:
                    walk_resp = requests.post(
                        f"{API_BASE}/chat/coord/walk",
                        json={
                            "start_coord": start_coord,
                            "max_steps": hop_count,
                            "current_coherence": 0.8
                        },
                        headers={"Content-Type": "application/json"}
                    )
                    walk_data = walk_resp.json()
                except Exception as e:
                    st.error(f"Backend handshake failed: {e}")
                    st.stop()

            path = walk_data.get("path") or walk_data.get("data", {}).get("path")

            if not path or not isinstance(path, list):
                st.warning("Backend returned no path. Simulating local traversal for demonstration.")
                path = [start_coord] + [f"WX-Simulated-Node-{i}" for i in range(1, hop_count + 1)]
            else:
                if path[0] != start_coord:
                    path.insert(0, start_coord)

            graph_placeholder = st.empty()
            status_placeholder = st.empty()

            dot = graphviz.Digraph(comment='Knowledge Walk')
            dot.attr(rankdir='LR')
            dot.attr('node', shape='box', style='filled', fillcolor='#f0fdf4', fontname='Courier New')

            visited_edges = set()

            for i, node_coord in enumerate(path):
                if i >= hop_count + 1:
                    break

                status_placeholder.markdown(f"**Hop {i}:** Resolving `{node_coord}`...")

                details = decode_coordinate(node_coord, silent=True)

                node_label = node_coord
                tooltip = "Unresolved"

                if details.get("status") == "success":
                    content = details.get("content", {})
                    claims = content.get("claims", [])
                    summary = content.get("summary", "")

                    if claims:
                        short_text = claims[0][:30] + "..." if len(claims[0]) > 30 else claims[0]
                    else:
                        short_text = summary[:30] + "..." if len(summary) > 30 else summary

                    node_label = f"{node_coord}\n[{short_text}]"
                    tooltip = summary

                if i == 0:
                    dot.node(node_coord, label=node_label, fillcolor='#dbeafe', tooltip=tooltip)
                else:
                    dot.node(node_coord, label=node_label, tooltip=tooltip)

                if i > 0:
                    prev_node = path[i - 1]
                    edge_key = f"{prev_node}-{node_coord}"
                    if edge_key not in visited_edges:
                        dot.edge(prev_node, node_coord, label=f"step {i}")
                        visited_edges.add(edge_key)

                graph_placeholder.graphviz_chart(dot)

                time.sleep(0.7)

            status_placeholder.success("Traversal Complete. Knowledge Tree Anchored.")
