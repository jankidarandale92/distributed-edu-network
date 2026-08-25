import sys
from pathlib import Path

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from gateway.server import search_all_nodes


st.set_page_config(
    page_title="EduShare",
    page_icon="🎓",
    layout="wide"
)


st.title("🎓 EduShare")

st.subheader(
    "Distributed Educational Resource Network"
)

st.write(
    "Search and access educational resources "
    "available across distributed nodes."
)

st.divider()


st.subheader(
    "Search Educational Resources"
)


query = st.text_input(
    "Enter a topic or keyword",
    placeholder="Example: Distributed Systems"
)


if st.button(
    "Search Resources",
    type="primary"
):

    if not query.strip():

        st.warning(
            "Please enter a search query."
        )

    else:

        with st.spinner(
            "Searching across distributed nodes..."
        ):

            resources = search_all_nodes(query)

        if not resources:

            st.warning(
                "No resources found."
            )

        else:

            st.success(
                f"{len(resources)} resource(s) found."
            )

            for resource in resources:

                with st.container(
                    border=True
                ):

                    st.subheader(
                        resource.title
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        st.write(
                            f"**Resource ID:** "
                            f"{resource.resource_id}"
                        )

                        st.write(
                            f"**Subject:** "
                            f"{resource.subject}"
                        )

                        st.write(
                            f"**Type:** "
                            f"{resource.resource_type}"
                        )

                    with col2:

                        st.write(
                            f"**Author:** "
                            f"{resource.author}"
                        )

                        st.write(
                            f"**Node:** "
                            f"{resource.node_id}"
                        )

                    if resource.description:

                        st.write(
                            f"**Description:** "
                            f"{resource.description}"
                        )