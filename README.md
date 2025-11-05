# PythonFS

Technical Interview Assignment:
Objective
● Design and implement a Python client application that runs as a long-lived
background service.
● This service must be fully containerized using Docker and orchestrated together with
a SeaweedFS cluster via Docker Compose.
Functional Requirements
● File Monitoring: Continuously monitor a designated local host directory (mounted as a
Docker volume) for the creation of new files.
● SeaweedFS Upload: Upload any newly detected file to the SeaweedFS cluster using its
HTTP API.
● Storage Reporting: Immediately after a successful upload, query the SeaweedFS
Master for cluster status and log the current total used storage space.
Additional Requirement (Host Routine Task)
● Implement a separate script or process (not containerized) that runs on the host
system.
● This task should periodically create new text files in the monitored directory at
random intervals between 30 and 60 seconds.

Environment Requirements
● The entire setup must run on Linux / Ubuntu.
