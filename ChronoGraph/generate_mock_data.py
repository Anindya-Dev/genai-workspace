import json
import random
from pathlib import Path
from datetime import datetime, timedelta

# ============================================================
# SETUP
# ============================================================

OUTPUT_DIR = Path("data/mock")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

random.seed(42)

users = [
    "rahul.sharma",
    "priya.patel",
    "anand.kumar",
    "neha.gupta",
    "vikram.singh",
    "arjun.mehta"
]

channels = [
    "#engineering",
    "#architecture",
    "#devops",
    "#cloud-migration"
]

slack = []
github = []
jira = []

slack_id = 1
pr_id = 1
jira_id = 1


# ============================================================
# HELPERS
# ============================================================

def random_date(start, end):
    delta = end - start
    return start + timedelta(
        days=random.randint(0, delta.days),
        hours=random.randint(9, 18),
        minutes=random.randint(0, 59)
    )


def add_slack(date, user, text, channel):
    global slack_id

    thread_ts = None
    if random.random() < 0.18:
        thread_ts = f"{int(date.timestamp())}.{random.randint(100000, 999999)}"

    slack.append({
        "id": f"slack_{slack_id:03}",
        "timestamp": date.isoformat(),
        "user": user,
        "text": text,
        "channel": channel,
        "thread_ts": thread_ts,
        "reactions": random.sample(
            ["thumbsup", "eyes", "thinking_face", "rocket", "white_check_mark"],
            k=random.randint(0, 2)
        ),
        "permalink": f"https://mock.slack/{slack_id:03}"
    })

    slack_id += 1


def add_pr(date, title, author):
    global pr_id
    status = random.choice([
        "merged",
        "merged",
        "merged",
        "closed",
        "open"
    ])
    repository = random.choice([
        "infra",
        "backend",
        "platform",
        "devops"
    ])
    merged_at = None
    if status == "merged":
        merged_dt = date + timedelta(days=random.randint(1, 5), hours=random.randint(1, 6))
        project_end = datetime(2023, 8, 31, 23, 59)
        merged_at = min(merged_dt, project_end).isoformat()

    github.append({
        "id": f"PR-{pr_id:03}",
        "title": title,
        "author": author,
        "created_at": date.isoformat(),
        "merged_at": merged_at,
        "status": status,
        "repository": repository,
        "description": f"{title}. Related to the AWS to GCP migration timeline and required production readiness checks.",
        "comments": [
            {
                "author": random.choice(users),
                "created_at": (date + timedelta(hours=2)).isoformat(),
                "body": "Please verify this against the migration runbook and rollback plan."
            },
            {
                "author": random.choice(users),
                "created_at": (date + timedelta(hours=6)).isoformat(),
                "body": "Looks good after reviewing the infrastructure impact and test results."
            }
        ],
        "labels": random.sample(
            ["gcp", "migration", "terraform", "kubernetes", "security", "monitoring", "database"],
            k=random.randint(1, 3)
        ),
        "url": f"https://mock.github/infotact/{repository}/pull/{pr_id}"
    })

    pr_id += 1


def add_jira(date, title, assignee, status):
    global jira_id
    done_at = date + timedelta(days=random.randint(3, 21))
    status_history = [
        {
            "status": "To Do",
            "changed_at": date.isoformat()
        }
    ]
    if status in ["In Progress", "Done"]:
        status_history.append({
            "status": "In Progress",
            "changed_at": (date + timedelta(days=1)).isoformat()
        })
    if status == "Done":
        status_history.append({
            "status": "Done",
            "changed_at": done_at.isoformat()
        })

    jira.append({
        "id": f"JIRA-{jira_id:03}",
        "title": title,
        "assignee": assignee,
        "status": status,
        "created_at": date.isoformat(),
        "updated_at": done_at.isoformat(),
        "description": f"{title}. Track implementation, validation evidence, owner, and migration impact.",
        "comments": [
            {
                "author": random.choice(users),
                "created_at": (date + timedelta(days=1)).isoformat(),
                "body": "Added acceptance criteria and linked this task to the migration milestone."
            },
            {
                "author": assignee,
                "created_at": (date + timedelta(days=2)).isoformat(),
                "body": "Work is progressing; dependencies and risks have been documented."
            }
        ],
        "status_history": status_history,
        "priority": random.choice(["High", "Medium", "Medium", "Low"]),
        "project": "CLOUD",
        "url": f"https://mock.jira/browse/JIRA-{jira_id:03}"
    })

    jira_id += 1


# ============================================================
# CORE STORY MESSAGES
# ============================================================

story_messages = [
    ("2023-01-10", "rahul.sharma",
     "Our AWS bill has increased by 40% in the last six months. We should evaluate alternatives."),

    ("2023-01-12", "neha.gupta",
     "I prepared a cost report and GCP appears significantly cheaper for compute workloads."),

    ("2023-01-15", "anand.kumar",
     "Maybe we should run a proof of concept on GCP."),

    ("2023-02-05", "priya.patel",
     "Migrating to GCP will require retraining the DevOps team."),

    ("2023-02-10", "vikram.singh",
     "There is a risk of production downtime during migration."),

    ("2023-02-15", "arjun.mehta",
     "Let's compare Kubernetes support on AWS and GCP."),

    ("2023-03-05", "anand.kumar",
     "The GCP proof of concept reduced compute costs by nearly 30%."),

    ("2023-03-10", "rahul.sharma",
     "Terraform modules can be migrated with minor changes."),

    ("2023-03-20", "neha.gupta",
     "Performance benchmarks on GCP look promising."),

    ("2023-04-10", "rahul.sharma",
     "Management has approved the AWS to GCP migration."),

    ("2023-04-15", "priya.patel",
     "We should begin planning the production migration."),

    ("2023-05-01", "anand.kumar",
     "I have started preparing Terraform updates for GCP."),

    ("2023-05-12", "vikram.singh",
     "Kubernetes migration plan has been finalized."),

    ("2023-06-01", "rahul.sharma",
     "The first production service has been migrated successfully."),

    ("2023-06-15", "priya.patel",
     "Monitoring dashboards have been updated for GCP."),

    ("2023-06-20", "anand.kumar",
     "Terraform deployment on GCP is stable."),

    ("2023-07-05", "neha.gupta",
     "Infrastructure costs have already dropped by 32%."),

    ("2023-07-15", "vikram.singh",
     "We can begin decommissioning old AWS resources."),

    ("2023-08-10", "rahul.sharma",
     "Final production workloads are now running on GCP."),

    ("2023-08-18", "vikram.singh",
     "AWS to GCP migration completed successfully.")
]

for date_str, user, text in story_messages:
    dt = datetime.fromisoformat(date_str)
    add_slack(
        dt,
        user,
        text,
        random.choice(channels)
    )


# ============================================================
# MONTH-BASED SLACK MESSAGES
# ============================================================

monthly_messages = {
    1: [
        "Our AWS bill increased by another 8% this month.",
        "Can someone prepare a cost comparison between AWS and GCP?",
        "We need to understand why compute costs are growing.",
        "Finance is asking for cloud cost optimization options."
    ],
    2: [
        "GCP pricing looks attractive for our workloads.",
        "Migration would require DevOps training.",
        "Terraform modules will need updates.",
        "We should evaluate Kubernetes support on GCP.",
        "I have concerns about migration risks."
    ],
    3: [
        "The proof of concept on GCP reduced compute costs by 30%.",
        "Performance tests on GCP look promising.",
        "The initial GKE setup is working well.",
        "We should present the PoC results to management."
    ],
    4: [
        "Management has approved the AWS to GCP migration.",
        "Let's start preparing the migration roadmap.",
        "We need to identify production dependencies.",
        "Migration planning meetings will begin next week."
    ],
    5: [
        "Terraform updates for GCP are underway.",
        "The Kubernetes migration plan is finalized.",
        "IAM roles have been configured in GCP.",
        "The migration runbook is ready for review.",
        "CI/CD pipelines are being updated."
    ],
    6: [
        "The first production service has been migrated successfully.",
        "Cloud SQL migration completed successfully.",
        "DNS cutover completed without downtime.",
        "Monitoring dashboards have been updated.",
        "Terraform deployments on GCP are stable."
    ],
    7: [
        "Infrastructure costs have dropped by 32%.",
        "Application latency has improved after migration.",
        "We should start decommissioning unused AWS resources.",
        "The GKE cluster is performing better than expected."
    ],
    8: [
        "All production services are now running on GCP.",
        "AWS resources can be decommissioned next week.",
        "The migration project has been completed successfully.",
        "Excellent work everyone on the migration effort."
    ]
}

while len(slack) < 112:
    month = random.randint(1, 8)

    date = datetime(
        2023,
        month,
        random.randint(1, 28),
        random.randint(9, 18),
        random.randint(0, 59)
    )

    user = random.choice(users)
    message = random.choice(monthly_messages[month])

    # Add realistic opinions
    if month == 2 and random.random() < 0.25:
        user = "vikram.singh"
        message = "I am concerned about production downtime during migration."

    elif month == 2 and random.random() < 0.20:
        user = "priya.patel"
        message = "The DevOps team will need training before we migrate to GCP."

    elif month == 3 and random.random() < 0.25:
        user = "anand.kumar"
        message = "The GCP proof of concept reduced compute costs by nearly 30%."

    elif month == 3 and random.random() < 0.20:
        user = "rahul.sharma"
        message = "The proof of concept demonstrates that GCP can handle our workloads."

    elif month == 5 and random.random() < 0.20:
        user = "rahul.sharma"
        message = "Terraform migration to GCP is progressing according to plan."

    elif month == 5 and random.random() < 0.20:
        user = "anand.kumar"
        message = "The Kubernetes migration checklist has been completed."

    elif month == 6 and random.random() < 0.20:
        user = "vikram.singh"
        message = "The DNS cutover was completed without any customer impact."

    elif month == 7 and random.random() < 0.20:
        user = "neha.gupta"
        message = "Infrastructure costs have dropped by more than 30% after migration."

    elif month == 8 and random.random() < 0.20:
        user = "vikram.singh"
        message = "All production services are now running successfully on GCP."

    add_slack(
        date,
        user,
        message,
        random.choice(channels)
    )

slack.sort(key=lambda x: x["timestamp"])


# ============================================================
# GITHUB PRS
# ============================================================

pr_titles = [
    "Add GCP Terraform configuration",
    "Configure Kubernetes manifests for GCP",
    "Add Cloud Monitoring dashboards",
    "Create Cloud SQL migration scripts",
    "Implement GCP IAM policies",
    "Add BigQuery analytics pipeline",
    "Migrate CI/CD pipelines to GCP",
    "Configure GKE autoscaling",
    "Add Cloud Storage backup jobs",
    "Refactor infrastructure modules",
    "Implement DNS cutover automation",
    "Create service account provisioning scripts",
    "Add VPC network configuration",
    "Implement GCP logging integration",
    "Configure Pub/Sub messaging",
    "Migrate Redis cache to Memorystore",
    "Implement disaster recovery workflow",
    "Optimize Kubernetes deployment manifests",
    "Add secret management integration",
    "Create infrastructure health checks",
    "Add migration smoke test workflow",
    "Document rollback automation scripts",
    "Configure workload identity federation",
    "Add production readiness checks",
    "Implement cloud cost alert rules"
]

start = datetime(2023, 1, 1)
end = datetime(2023, 8, 31)

for title in pr_titles:
    add_pr(
        random_date(start, end),
        title,
        random.choice(users)
    )

github.sort(key=lambda x: x["created_at"])


# ============================================================
# JIRA TICKETS
# ============================================================

jira_titles = [
    "Evaluate GCP migration feasibility",
    "Prepare AWS vs GCP cost comparison report",
    "Build proof of concept on GCP",
    "Create migration runbook",
    "Migrate Kubernetes cluster to GCP",
    "Configure GCP IAM roles",
    "Move monitoring stack to GCP",
    "Update Terraform modules",
    "Implement DNS cutover plan",
    "Migrate Cloud SQL database",
    "Create BigQuery datasets",
    "Configure service accounts",
    "Update CI/CD pipelines",
    "Implement backup strategy",
    "Migrate Redis cache",
    "Create disaster recovery procedures",
    "Implement centralized logging",
    "Set up GKE cluster",
    "Configure VPC networking",
    "Create cost monitoring dashboard",
    "Perform load testing on GCP",
    "Validate production deployment",
    "Migrate object storage",
    "Configure alerting policies",
    "Optimize compute resources",
    "Decommission AWS resources",
    "Update engineering documentation",
    "Implement security scanning",
    "Migrate analytics workloads",
    "Finalize production cutover",
    "Review migration risk register",
    "Document rollback communication plan",
    "Validate GKE autoscaling policy",
    "Create post-migration cost report",
    "Confirm AWS decommission checklist"
]

for title in jira_titles:
    add_jira(
        random_date(start, end),
        title,
        random.choice(users),
        random.choice([
            "To Do",
            "In Progress",
            "Done"
        ])
    )

jira.sort(key=lambda x: x["created_at"])


# ============================================================
# SAVE FILES
# ============================================================

with open(OUTPUT_DIR / "mock_slack.json", "w") as f:
    json.dump({"messages": slack}, f, indent=2)

with open(OUTPUT_DIR / "mock_github.json", "w") as f:
    json.dump({"pull_requests": github}, f, indent=2)

with open(OUTPUT_DIR / "mock_jira.json", "w") as f:
    json.dump({"tickets": jira}, f, indent=2)

print("Realistic mock data generated successfully.")
print("Files saved in data/mock/")
