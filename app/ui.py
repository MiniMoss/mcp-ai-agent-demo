import gradio as gr
from gmail_send import my_crew 
from github_star import github_task, github_crew
import time
from crewai import Task

def send_email_ui(to, subject, body):
    # Validation checks
    if not to.strip():
        raise gr.Error("Recipient email address cannot be empty")
    if not subject.strip():
        raise gr.Error("Email subject cannot be empty")
    
    # Basic email format validation
    if "@" not in to or "." not in to:
        raise gr.Error("Please enter a valid email address")

    email_task = Task(
        description=f"Send an email to {to} with subject '{subject}' and body '{body}'",
        agent=my_crew.agents[0],
        expected_output="Confirmation that the email was sent successfully"
    )
    my_crew.tasks = [email_task]

    try:
        yield "⏳ Sending email, please wait..."
        time.sleep(1)  # Small delay to show the loading state
        result = my_crew.kickoff()
        yield f"✅ {result}"
    except Exception as e:
        raise gr.Error(f"Failed to send email: {str(e)}")

def clear_form():
    return "", "", "", "Ready to compose new email", ""  # Returns empty values for all fields including status and output_box

def star_github_repo(repo_url):
    # Validation checks
    if not repo_url.strip():
        raise ValueError("GitHub repository URL cannot be empty")

    github_task.description = f"Star the GitHub repository {repo_url} for the authenticated user"
    github_crew.tasks = [github_task]

    try:
        result = github_crew.kickoff()
        return f"✅ {result}"
    except Exception as e:
        raise ValueError(f"Failed to star repository: {str(e)}")

with gr.Blocks() as demo:
    gr.Markdown("# 📬 MCP AI Agent Demo (CrewAI + Composio + Gradio)")

    with gr.Tab("Send Email"):
        with gr.Row():
            to_input = gr.Textbox(label="Recipient Email*", lines=1, placeholder="recipient@example.com", info="Required field")
        with gr.Row():
            subject_input = gr.Textbox(label="Subject*", lines=1, placeholder="Enter email subject", info="Required field")
        with gr.Row():
            body_input = gr.Textbox(label="Email Body", lines=5, placeholder="Enter email content")
        
        # Status output
        status_output = gr.Textbox(label="Status", visible=True, interactive=False)
        
        with gr.Row():
            send_btn = gr.Button("Send Email", variant="primary")
            new_email_btn = gr.Button("New Email", variant="secondary")
        
        output_box = gr.Textbox(label="Result", lines=5, interactive=False)
        
        # Form validation and submission
        email_sender = send_btn.click(
            fn=send_email_ui, 
            inputs=[to_input, subject_input, body_input], 
            outputs=[status_output],
            api_name="send_email"
        ).then(
            lambda x: x,
            inputs=[status_output],
            outputs=[output_box]
        )
        
        # Disable send button during processing
        email_sender.then(
            lambda: gr.Button(interactive=True),
            inputs=None,
            outputs=[send_btn]
        )
        
        # New email button action - clears ALL fields including status
        new_email_btn.click(
            fn=clear_form,
            inputs=None,
            outputs=[to_input, subject_input, body_input, status_output, output_box],
            queue=False
        )
        
        # Prevent double clicks
        send_btn.click(
            lambda: gr.Button(interactive=False),
            inputs=None,
            outputs=[send_btn],
            queue=False
        )

    with gr.Tab("GitHub Star Repo"):
        with gr.Row():
            repo_url_input = gr.Textbox(label="GitHub Repository URL*", lines=1, placeholder="https://github.com/username/repo", info="Required field")
        
        # Status output
        github_status_output = gr.Textbox(label="Status", visible=True, interactive=False)
        
        with gr.Row():
            star_repo_btn = gr.Button("Star Repository", variant="primary")
        
        github_output_box = gr.Textbox(label="Result", lines=5, interactive=False)
        
        # Form validation and submission
        github_star_action = star_repo_btn.click(
            fn=star_github_repo, 
            inputs=[repo_url_input], 
            outputs=[github_status_output],
            api_name="star_github_repo"
        ).then(
            lambda x: x,
            inputs=[github_status_output],
            outputs=[github_output_box]
        )
        
        # Disable star button during processing
        github_star_action.then(
            lambda: gr.Button(interactive=True),
            inputs=None,
            outputs=[star_repo_btn]
        )
        
        # Prevent double clicks
        star_repo_btn.click(
            lambda: gr.Button(interactive=False),
            inputs=None,
            outputs=[star_repo_btn],
            queue=False
        )

demo.launch(server_name="0.0.0.0", server_port=7860)