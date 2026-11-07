
import streamlit as st

from database import (
    init_db,
    create_incident,
    save_outcome,
    update_memory_status
)

from memory import retain_memory
from investigator import investigate_incident


# -----------------------------
# PAGE CONFIGURATION
# -----------------------------

st.set_page_config(
    page_title="Scar Tissue | AI Incident Investigator",
    page_icon="🩹",
    layout="wide"
)

init_db()


# -----------------------------
# SESSION STATE
# -----------------------------

if "active_incident" not in st.session_state:
    st.session_state.active_incident = None

if "saved_outcome" not in st.session_state:
    st.session_state.saved_outcome = None


# -----------------------------
# PAGE HEADER
# -----------------------------

st.title("🩹 Scar Tissue")
st.subheader("AI-Powered Incident Investigation")

st.write(
    "Learn from previous incidents. Investigate smarter. "
    "Build organizational memory."
)

st.divider()


# -----------------------------
# INCIDENT REPORTING
# -----------------------------

st.header("1. Report an Incident")

with st.form("incident_form"):

    service = st.text_input(
        "Affected Service",
        placeholder="Example: Checkout API"
    )

    description = st.text_area(
        "Problem Description",
        placeholder="Describe what went wrong..."
    )

    observations = st.text_area(
        "Logs and Current Observations",
        placeholder="Enter error messages, metrics, logs..."
    )

    use_history = st.checkbox(
        "Use historical incident memories from Hindsight",
        value=True
    )

    investigate_button = st.form_submit_button(
        "🔍 Investigate Incident",
        use_container_width=True
    )


if investigate_button:

    if not service.strip() or not description.strip():
        st.error("Please enter the service and problem description.")

    else:
        with st.spinner(
            "Retrieving memories and investigating the incident..."
        ):

            try:
                result = investigate_incident(
                    service=service,
                    description=description,
                    observations=observations,
                    use_history=use_history
                )

                incident_id = create_incident(
                    service,
                    description,
                    observations
                )

                st.session_state.active_incident = {
                    "id": incident_id,
                    "service": service,
                    "description": description,
                    "observations": observations,
                    "result": result
                }

                st.session_state.saved_outcome = None

                st.success("Investigation completed successfully!")

            except Exception as error:
                st.error(
                    "Investigation could not be completed. "
                    "Please check your API connection and try again."
                )
                st.caption(str(error))


# -----------------------------
# INVESTIGATION REPORT
# -----------------------------

incident = st.session_state.active_incident

if incident:

    st.divider()
    st.header("2. Investigation Results")

    st.caption(f"Incident ID: {incident['id']}")

    st.subheader("AI Investigation Report")

    st.markdown(incident["result"]["report"])

    st.subheader("Retrieved Historical Experiences")

    memories = incident["result"]["memories"]

    if memories:

        for index, memory in enumerate(memories, start=1):

            with st.expander(
                f"Memory {index} — {memory['type'].title()}"
            ):
                st.write(memory["text"])

    else:
        st.info("No relevant historical memories found.")

    st.divider()


    # -----------------------------
    # RECORD ENGINEER OUTCOME
    # -----------------------------

    st.header("3. Record Investigation Outcome")

    st.write(
        "Record what the engineer actually tried and what happened. "
        "Only enter a confirmed cause if it has been verified."
    )

    saved_outcome = st.session_state.saved_outcome

    if not saved_outcome:

        with st.form("outcome_form"):

            action = st.text_area(
                "Action Attempted",
                placeholder="Example: Checked database connection pool..."
            )

            outcome_status = st.selectbox(
                "Outcome Status",
                [
                    "Failed",
                    "Temporary relief",
                    "Resolved",
                    "Unknown"
                ]
            )

            observed_result = st.text_area(
                "What Happened?",
                placeholder="Describe the result of the action..."
            )

            confirmed_cause = st.text_area(
                "Confirmed Root Cause (if known)",
                placeholder="Leave blank if the cause is not confirmed..."
            )

            save_button = st.form_submit_button(
                "💾 Save Outcome to Memory",
                use_container_width=True
            )

        if save_button:

            if not action.strip():
                st.error("Please enter the action attempted.")

            elif not observed_result.strip():
                st.error("Please describe what happened.")

            else:

                try:
                    outcome_id = save_outcome(
                        incident_id=incident["id"],
                        action_attempted=action,
                        outcome_status=outcome_status,
                        observed_result=observed_result,
                        confirmed_cause=confirmed_cause
                    )

                    # Keep the memory content explicit and factual.
                    memory_content = f"""
Incident ID: {incident['id']}
Service: {incident['service']}
Problem: {incident['description']}
Initial observations: {incident['observations']}

Action attempted by engineer: {action}
Outcome status: {outcome_status}
Observed result: {observed_result}
Engineer-confirmed root cause: {
    confirmed_cause if confirmed_cause.strip()
    else "Not confirmed"
}
"""

                    st.session_state.saved_outcome = {
                        "outcome_id": outcome_id,
                        "content": memory_content,
                        "sync_status": "pending"
                    }

                    st.rerun()

                except Exception as error:
                    st.error(f"Could not save outcome: {error}")


    # -----------------------------
    # HINDSIGHT MEMORY SYNC
    # -----------------------------

    saved_outcome = st.session_state.saved_outcome

    if saved_outcome:

        if saved_outcome["sync_status"] == "pending":

            try:
                response = retain_memory(
                    saved_outcome["content"],
                    context="Scar Tissue verified incident outcome"
                )

                if not response.success:
                    raise RuntimeError(
                        "Hindsight did not confirm memory retention."
                    )

                update_memory_status(
                    saved_outcome["outcome_id"],
                    "saved"
                )

                saved_outcome["sync_status"] = "saved"

            except Exception as error:

                update_memory_status(
                    saved_outcome["outcome_id"],
                    "failed"
                )

                saved_outcome["sync_status"] = "failed"
                saved_outcome["error"] = str(error)

        if saved_outcome["sync_status"] == "saved":

            st.success(
                "Outcome saved in SQLite and successfully retained "
                "in Hindsight!"
            )

        elif saved_outcome["sync_status"] == "failed":

            st.warning(
                "Outcome is safely stored in SQLite, but Hindsight "
                "synchronization failed."
            )

            st.caption(saved_outcome.get("error", ""))

            if st.button("🔄 Retry Hindsight Sync"):

                try:
                    response = retain_memory(
                        saved_outcome["content"],
                        context="Scar Tissue verified incident outcome"
                    )

                    if not response.success:
                        raise RuntimeError(
                            "Hindsight did not confirm memory retention."
                        )

                    update_memory_status(
                        saved_outcome["outcome_id"],
                        "saved"
                    )

                    saved_outcome["sync_status"] = "saved"
                    st.success("Memory synchronization successful!")

                except Exception as error:
                    st.error(f"Retry failed: {error}")


# -----------------------------
# FOOTER
# -----------------------------

st.divider()

st.caption(
    "Scar Tissue | AI-assisted incident investigation "
    "and persistent organizational memory"
)
