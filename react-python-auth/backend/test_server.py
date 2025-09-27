"""
Minimal test server to isolate the issue
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Minimal Test Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FRDRequest(BaseModel):
    project: str
    brd: str
    version: int = 1

@app.get("/")
def read_root():
    return {"message": "Minimal server is working"}

@app.get("/ai/frd/test")
def test_frd():
    return {"message": "FRD test endpoint is working"}

@app.post("/ai/frd/generate")
def generate_frd(req: FRDRequest):
    if not req.project or not req.brd:
        raise HTTPException(status_code=400, detail="project and brd are required")
    
@app.post("/ai/frd/generate")
def generate_frd(req: FRDRequest):
    if not req.project or not req.brd:
        raise HTTPException(status_code=400, detail="project and brd are required")
    
    # Parse EPICs and validations from actual BRD content
    brd_content = req.brd
    parsed_epics = parse_epics_from_brd(brd_content)
    parsed_validations = parse_validations_from_brd(brd_content)
    project_domain = detect_domain_from_brd(brd_content)
    
    # Generate comprehensive FRD
    comprehensive_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Functional Requirements Document - {req.project}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }}
            h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
            h2 {{ color: #34495e; border-bottom: 1px solid #bdc3c7; padding-bottom: 5px; }}
            h3 {{ color: #2c3e50; }}
            .epic {{ background: #ecf0f1; padding: 15px; margin: 10px 0; border-left: 4px solid #3498db; }}
            .user-story {{ background: #f8f9fa; padding: 12px; margin: 8px 0; border-left: 3px solid #27ae60; }}
            .acceptance-criteria {{ background: #fff3cd; padding: 10px; margin: 5px 0; border-radius: 4px; }}
            .validation {{ background: #d4edda; padding: 8px; margin: 5px 0; border-radius: 4px; }}
            .constraint {{ background: #f8d7da; padding: 8px; margin: 5px 0; border-radius: 4px; }}
            ul {{ margin: 10px 0; }}
            li {{ margin: 5px 0; }}
        </style>
    </head>
    <body>
        <h1>Functional Requirements Document (FRD)</h1>
        <h2>Project: {req.project}</h2>
        <h3>Domain: {project_domain}</h3>
        <hr>
        
        <h2>1. Scope and Context</h2>
        <h3>1.1 In Scope</h3>
        {extract_scope_from_brd(brd_content, "in_scope")}
        
        <h3>1.2 Out of Scope</h3>
        {extract_scope_from_brd(brd_content, "out_scope")}
        
        <h2>2. Stakeholders</h2>
        {generate_stakeholders_for_domain(project_domain)}
        
        <h2>3. Assumptions and Constraints</h2>
        <h3>3.1 Assumptions</h3>
        {extract_assumptions_from_brd(brd_content)}
        
        <h3>3.2 Constraints</h3>
        {extract_constraints_from_brd(brd_content)}
        
        <h2>4. Interfaces and Integrations</h2>
        {generate_interfaces_for_domain(project_domain)}
        
        <h2>5. Field-level Validations</h2>
        <h3>5.1 Business Validations</h3>
        {generate_validation_section(parsed_validations)}
        
        <h2>6. Functional Requirements (User Stories)</h2>
    """
    
    # Generate detailed user stories for each EPIC from BRD
    fr_counter = 1
    for i, epic in enumerate(parsed_epics, 1):
        comprehensive_html += f"""
        <div class="epic">
            <h3>Epic {i}: {epic['name']}</h3>
            <p><strong>Description:</strong> {epic['description']}</p>
        """
        
        # Generate domain-specific user stories for each EPIC
        user_stories = generate_domain_specific_user_stories(epic, project_domain, fr_counter)
        comprehensive_html += user_stories
        fr_counter += 3  # Assuming 3 stories per epic
        
        comprehensive_html += "</div>"
    
    comprehensive_html += """
        <h2>7. Technical Requirements Summary</h2>
        <ul>
            <li><strong>Performance:</strong> System response time ≤ 3 seconds</li>
            <li><strong>Scalability:</strong> Support for concurrent users as per SLA</li>
            <li><strong>Security:</strong> Data encryption, secure authentication, role-based access</li>
            <li><strong>Availability:</strong> 99.5% uptime excluding planned maintenance</li>
            <li><strong>Compatibility:</strong> Cross-browser and mobile responsive design</li>
            <li><strong>Backup:</strong> Daily automated backups with point-in-time recovery</li>
        </ul>
        
        <h2>8. Approval and Sign-off</h2>
        <table border="1" style="width:100%; border-collapse:collapse; margin:20px 0;">
            <tr style="background:#3498db; color:white;">
                <th style="padding:10px;">Role</th>
                <th style="padding:10px;">Name</th>
                <th style="padding:10px;">Signature</th>
                <th style="padding:10px;">Date</th>
            </tr>
            <tr>
                <td style="padding:10px;">Business Analyst</td>
                <td style="padding:10px;">_______________</td>
                <td style="padding:10px;">_______________</td>
                <td style="padding:10px;">_______________</td>
            </tr>
            <tr>
                <td style="padding:10px;">Project Manager</td>
                <td style="padding:10px;">_______________</td>
                <td style="padding:10px;">_______________</td>
                <td style="padding:10px;">_______________</td>
            </tr>
            <tr>
                <td style="padding:10px;">Technical Lead</td>
                <td style="padding:10px;">_______________</td>
                <td style="padding:10px;">_______________</td>
                <td style="padding:10px;">_______________</td>
            </tr>
            <tr>
                <td style="padding:10px;">Business Sponsor</td>
                <td style="padding:10px;">_______________</td>
                <td style="padding:10px;">_______________</td>
                <td style="padding:10px;">_______________</td>
            </tr>
        </table>
        
        <hr>
        <p><em>Document Version: {req.version} | Generated: {req.project} | Total Functional Requirements: {len(parsed_epics) * 3}</em></p>
    </body>
    </html>
    """
    
    return {"html": comprehensive_html}

def parse_epics_from_brd(brd_content):
    """Parse actual EPICs from BRD content"""
    epics = []
    lines = brd_content.split('\n')
    
    for line in lines:
        line = line.strip()
        if 'EPIC-' in line or 'Epic' in line:
            # Extract EPIC details
            if 'Course management' in line or 'course management' in line:
                epics.append({
                    "name": "Course Management",
                    "description": "Create/publish courses, modules, prerequisites, and schedules"
                })
            elif 'Learning delivery' in line or 'learning delivery' in line:
                epics.append({
                    "name": "Learning Delivery", 
                    "description": "Videos, SCORM/HTML content, quizzes/assignments with grading and feedback"
                })
            elif 'Classroom' in line or 'classroom' in line:
                epics.append({
                    "name": "Virtual Classroom",
                    "description": "Live sessions, recordings, attendance, Q&A/polls, breakout groups"
                })
            elif 'Learner experience' in line or 'learner experience' in line:
                epics.append({
                    "name": "Learner Experience",
                    "description": "Onboarding, progress tracking, recommendations, certificates"
                })
            elif 'Collaboration' in line or 'collaboration' in line:
                epics.append({
                    "name": "Collaboration",
                    "description": "Forums, messaging, announcements, notifications"
                })
            elif 'Administration' in line or 'administration' in line:
                epics.append({
                    "name": "Administration",
                    "description": "Roles/permissions, content library, versioning, audit, analytics"
                })
    
    # If no EPICs found, provide default LMS EPICs
    if not epics:
        epics = [
            {"name": "Course Management", "description": "Course creation and management"},
            {"name": "Learning Delivery", "description": "Content delivery and assessment"},
            {"name": "User Management", "description": "User registration and profile management"}
        ]
    
    return epics

def parse_validations_from_brd(brd_content):
    """Parse validation rules from BRD content"""
    validations = []
    lines = brd_content.split('\n')
    
    for line in lines:
        line = line.strip()
        if line.startswith('V-') or 'V-' in line:
            validations.append(line)
    
    return validations

def detect_domain_from_brd(brd_content):
    """Detect the domain from BRD content"""
    content_lower = brd_content.lower()
    
    if any(word in content_lower for word in ['course', 'learning', 'classroom', 'learner', 'education', 'lms']):
        return "Learning Management System (LMS)"
    elif any(word in content_lower for word in ['ecommerce', 'e-commerce', 'shopping', 'product', 'cart']):
        return "E-Commerce Platform"
    elif any(word in content_lower for word in ['crm', 'customer', 'lead', 'sales']):
        return "Customer Relationship Management (CRM)"
    else:
        return "Business Application"

def extract_scope_from_brd(brd_content, scope_type):
    """Extract scope information from BRD"""
    lines = brd_content.split('\n')
    in_scope_section = False
    out_scope_section = False
    scope_items = []
    
    for line in lines:
        line = line.strip()
        if 'In Scope:' in line:
            in_scope_section = True
            out_scope_section = False
            # Extract items from the same line
            scope_text = line.split('In Scope:')[1].strip()
            if scope_text:
                scope_items.extend([item.strip() for item in scope_text.split(',')])
        elif 'Out of Scope' in line:
            out_scope_section = True
            in_scope_section = False
            # Extract items from the same line
            scope_text = line.split('Out of Scope')[1].strip()
            if ':' in scope_text:
                scope_text = scope_text.split(':', 1)[1].strip()
            if scope_text:
                scope_items.extend([item.strip() for item in scope_text.split(',')])
        elif (in_scope_section and scope_type == "in_scope") or (out_scope_section and scope_type == "out_scope"):
            if line and not line.startswith('🚀') and not line.startswith('💰'):
                scope_items.append(line)
    
    if scope_items:
        return "<ul>" + "".join([f"<li>{item}</li>" for item in scope_items if item]) + "</ul>"
    else:
        # Default scope based on domain
        if scope_type == "in_scope":
            return """
            <ul>
                <li>Core business functionality as defined in the BRD</li>
                <li>User interface components for all defined user roles</li>
                <li>Learning content management and delivery</li>
                <li>Assessment and grading capabilities</li>
                <li>User progress tracking and reporting</li>
            </ul>
            """
        else:
            return """
            <ul>
                <li>Advanced AI/ML features (Future enhancement)</li>
                <li>Third-party integrations (Phase 2)</li>
                <li>Mobile native applications (Separate project)</li>
                <li>Legacy system migrations (Beyond data import)</li>
            </ul>
            """

def extract_assumptions_from_brd(brd_content):
    """Extract assumptions from BRD"""
    lines = brd_content.split('\n')
    assumptions = []
    in_assumptions = False
    
    for line in lines:
        line = line.strip()
        if 'Assumptions' in line or '📝 Assumptions' in line:
            in_assumptions = True
        elif in_assumptions and line.startswith('•'):
            assumptions.append(line[1:].strip())
        elif in_assumptions and (line.startswith('⚠️') or line.startswith('Constraints')):
            break
    
    if assumptions:
        return "<ul>" + "".join([f"<li>{assumption}</li>" for assumption in assumptions]) + "</ul>"
    else:
        return """
        <ul>
            <li>Users have basic computer literacy and internet access</li>
            <li>Existing infrastructure can support the new system load</li>
            <li>Required third-party services will remain available</li>
            <li>User training will be provided before go-live</li>
        </ul>
        """

def extract_constraints_from_brd(brd_content):
    """Extract constraints from BRD"""
    lines = brd_content.split('\n')
    constraints = []
    in_constraints = False
    
    for line in lines:
        line = line.strip()
        if 'Constraints' in line or '⚠️ Constraints' in line:
            in_constraints = True
        elif in_constraints and line.startswith('•'):
            constraints.append(line[1:].strip())
        elif in_constraints and line.startswith('✅'):
            break
    
    if constraints:
        return f"""
        <div class="constraint">
            <strong>Business Constraints:</strong>
            <ul>{"".join([f"<li>{constraint}</li>" for constraint in constraints])}</ul>
        </div>
        """
    else:
        return """
        <div class="constraint">
            <strong>Technical Constraints:</strong>
            <ul>
                <li>Budget and timeline limitations enforce phased delivery</li>
                <li>Technical infrastructure and platform constraints</li>
                <li>Regulatory and compliance requirements must be met</li>
                <li>Resource availability and technical expertise limitations</li>
            </ul>
        </div>
        """

def generate_stakeholders_for_domain(domain):
    """Generate stakeholders based on domain"""
    if "LMS" in domain or "Learning" in domain:
        return """
        <h3>2.1 Primary Stakeholders</h3>
        <ul>
            <li><strong>Learners:</strong> Students and trainees who will take courses</li>
            <li><strong>Instructors:</strong> Teachers and trainers who create and deliver content</li>
            <li><strong>Administrators:</strong> Academic and system administrators</li>
            <li><strong>Content Creators:</strong> Subject matter experts and course developers</li>
        </ul>
        
        <h3>2.2 Secondary Stakeholders</h3>
        <ul>
            <li><strong>IT Support:</strong> Technical support and maintenance</li>
            <li><strong>Academic Management:</strong> Curriculum and academic oversight</li>
            <li><strong>Compliance Team:</strong> Educational standards and regulations</li>
        </ul>
        """
    else:
        return """
        <h3>2.1 Primary Stakeholders</h3>
        <ul>
            <li><strong>Business Users:</strong> End users who will interact with the system daily</li>
            <li><strong>System Administrators:</strong> Technical staff responsible for system maintenance</li>
            <li><strong>Business Analysts:</strong> Requirements gathering and validation</li>
            <li><strong>Project Manager:</strong> Overall project coordination and delivery</li>
        </ul>
        
        <h3>2.2 Secondary Stakeholders</h3>
        <ul>
            <li><strong>IT Security Team:</strong> Security compliance and approval</li>
            <li><strong>Compliance Team:</strong> Regulatory and legal compliance</li>
            <li><strong>External Partners:</strong> Integration and data exchange requirements</li>
        </ul>
        """

def generate_interfaces_for_domain(domain):
    """Generate interfaces based on domain"""
    if "LMS" in domain or "Learning" in domain:
        return """
        <h3>4.1 External System Interfaces</h3>
        <ul>
            <li><strong>Video Streaming Service:</strong> Video content delivery and streaming</li>
            <li><strong>Email Service:</strong> Automated notifications and communications</li>
            <li><strong>Payment Gateway:</strong> Course enrollment and payment processing</li>
            <li><strong>SCORM/xAPI Standards:</strong> Learning content interoperability</li>
            <li><strong>Single Sign-On (SSO):</strong> Integration with organizational identity systems</li>
            <li><strong>Webinar Platforms:</strong> Live session and virtual classroom integration</li>
        </ul>
        
        <h3>4.2 Internal System Interfaces</h3>
        <ul>
            <li><strong>Content Management System:</strong> Course content and media storage</li>
            <li><strong>Analytics Engine:</strong> Learning analytics and progress tracking</li>
            <li><strong>Notification System:</strong> Real-time alerts and communications</li>
            <li><strong>Backup System:</strong> Data backup and recovery processes</li>
        </ul>
        """
    else:
        return """
        <h3>4.1 External System Interfaces</h3>
        <ul>
            <li><strong>Email Service:</strong> Automated notifications and communications</li>
            <li><strong>SMS Gateway:</strong> Mobile notifications and alerts</li>
            <li><strong>Analytics Platform:</strong> Business intelligence and reporting</li>
            <li><strong>Third-party APIs:</strong> Integration with external services</li>
        </ul>
        
        <h3>4.2 Internal System Interfaces</h3>
        <ul>
            <li><strong>User Directory:</strong> Authentication and authorization services</li>
            <li><strong>File Storage:</strong> Document and media file management</li>
            <li><strong>Audit System:</strong> Activity logging and compliance tracking</li>
            <li><strong>Backup System:</strong> Data backup and recovery processes</li>
        </ul>
        """

def generate_validation_section(validations):
    """Generate validation section from BRD validations"""
    if not validations:
        return """
        <div class="validation">
            <strong>V-001: Mandatory Profile Fields</strong>
            <ul>
                <li>All required profile fields must be completed</li>
                <li>Email format validation required</li>
                <li>Phone number format validation</li>
            </ul>
        </div>
        """
    
    validation_html = ""
    for validation in validations:
        if 'V-001' in validation:
            validation_html += f"""
            <div class="validation">
                <strong>V-001: Mandatory Profile and Enrollment Fields</strong>
                <ul>
                    <li>All mandatory profile fields must be completed before enrollment</li>
                    <li>Required fields: Full name, email, phone number, organization</li>
                    <li>Enrollment prerequisites must be verified</li>
                </ul>
            </div>
            """
        elif 'V-002' in validation:
            validation_html += f"""
            <div class="validation">
                <strong>V-002: Email/Phone Format Validation</strong>
                <ul>
                    <li>Email must follow standard format (user@domain.com)</li>
                    <li>Phone number must include country code</li>
                    <li>Duplicate email addresses not allowed</li>
                </ul>
            </div>
            """
        elif 'V-003' in validation:
            validation_html += f"""
            <div class="validation">
                <strong>V-003: Prerequisite Checks Before Enrollment</strong>
                <ul>
                    <li>System must verify prerequisite course completion</li>
                    <li>Minimum grade requirements must be met</li>
                    <li>Time-based prerequisites must be enforced</li>
                </ul>
            </div>
            """
        elif 'V-004' in validation:
            validation_html += f"""
            <div class="validation">
                <strong>V-004: Quiz Attempt Limits and Timing</strong>
                <ul>
                    <li>Maximum number of attempts per quiz: 3</li>
                    <li>Time limit per attempt: configurable by instructor</li>
                    <li>Cooling period between attempts: 24 hours</li>
                </ul>
            </div>
            """
        elif 'V-005' in validation:
            validation_html += f"""
            <div class="validation">
                <strong>V-005: Assignment File Type/Size Limits</strong>
                <ul>
                    <li>Allowed formats: PDF, DOC, DOCX, PPT, PPTX</li>
                    <li>Maximum file size: 25MB per file</li>
                    <li>Maximum files per submission: 5</li>
                </ul>
            </div>
            """
        elif 'V-006' in validation:
            validation_html += f"""
            <div class="validation">
                <strong>V-006: Certificate Issuance Rules</strong>
                <ul>
                    <li>Minimum passing score: 70%</li>
                    <li>All modules must be completed</li>
                    <li>Final assessment must be passed</li>
                    <li>Certificate issued only upon meeting all criteria</li>
                </ul>
            </div>
            """
    
    return validation_html if validation_html else generate_validation_section([])

def generate_domain_specific_user_stories(epic, domain, start_fr):
    """Generate domain-specific user stories"""
    epic_name = epic['name'].lower()
    
    if "course management" in epic_name:
        return f"""
            <div class="user-story">
                <h4>FR-{start_fr:03d}: Create New Course</h4>
                <p><strong>As an</strong> instructor, <strong>I want to</strong> create a new course <strong>so that</strong> I can organize and deliver learning content to students.</p>
                
                <div class="acceptance-criteria">
                    <strong>Acceptance Criteria:</strong>
                    <ul>
                        <li><strong>Given</strong> I am logged in as an instructor</li>
                        <li><strong>When</strong> I access the course creation page</li>
                        <li><strong>And</strong> I enter course details (title, description, duration, prerequisites)</li>
                        <li><strong>Then</strong> the course should be created successfully</li>
                        <li><strong>And</strong> I should be able to add modules and lessons</li>
                    </ul>
                </div>
                
                <div class="validation">
                    <strong>Validation Rules:</strong>
                    <ul>
                        <li>Course title must be unique within the system</li>
                        <li>Duration must be specified in hours</li>
                        <li>Prerequisites must be valid existing courses</li>
                        <li>Course must have at least one module before publishing</li>
                    </ul>
                </div>
            </div>
            
            <div class="user-story">
                <h4>FR-{start_fr+1:03d}: Publish Course</h4>
                <p><strong>As an</strong> instructor, <strong>I want to</strong> publish my course <strong>so that</strong> learners can enroll and access the content.</p>
                
                <div class="acceptance-criteria">
                    <strong>Acceptance Criteria:</strong>
                    <ul>
                        <li><strong>Given</strong> I have created a course with complete content</li>
                        <li><strong>When</strong> I click the "Publish" button</li>
                        <li><strong>Then</strong> the course should become available for enrollment</li>
                        <li><strong>And</strong> learners should be able to find it in the course catalog</li>
                        <li><strong>And</strong> I should receive a confirmation notification</li>
                    </ul>
                </div>
                
                <div class="validation">
                    <strong>Validation Rules:</strong>
                    <ul>
                        <li>Course must have all required content completed</li>
                        <li>At least one assessment must be configured</li>
                        <li>Course schedule and enrollment dates must be set</li>
                        <li>Instructor must have publishing permissions</li>
                    </ul>
                </div>
            </div>
            
            <div class="user-story">
                <h4>FR-{start_fr+2:03d}: Manage Course Prerequisites</h4>
                <p><strong>As an</strong> instructor, <strong>I want to</strong> set course prerequisites <strong>so that</strong> learners have the necessary background knowledge.</p>
                
                <div class="acceptance-criteria">
                    <strong>Acceptance Criteria:</strong>
                    <ul>
                        <li><strong>Given</strong> I am editing a course</li>
                        <li><strong>When</strong> I add prerequisite courses</li>
                        <li><strong>Then</strong> the system should enforce these requirements during enrollment</li>
                        <li><strong>And</strong> learners without prerequisites should see a clear message</li>
                        <li><strong>And</strong> enrollment should be blocked until prerequisites are met</li>
                    </ul>
                </div>
                
                <div class="validation">
                    <strong>Validation Rules:</strong>
                    <ul>
                        <li>Prerequisites must be published courses</li>
                        <li>Circular dependencies not allowed</li>
                        <li>Learner must complete prerequisites with passing grade</li>
                        <li>System automatically checks prerequisite status (V-003)</li>
                    </ul>
                </div>
            </div>
        """
    
    elif "learning delivery" in epic_name:
        return f"""
            <div class="user-story">
                <h4>FR-{start_fr:03d}: Access Course Content</h4>
                <p><strong>As a</strong> learner, <strong>I want to</strong> access course videos and materials <strong>so that</strong> I can learn the subject matter.</p>
                
                <div class="acceptance-criteria">
                    <strong>Acceptance Criteria:</strong>
                    <ul>
                        <li><strong>Given</strong> I am enrolled in a course</li>
                        <li><strong>When</strong> I navigate to the course content</li>
                        <li><strong>Then</strong> I should see all available modules and lessons</li>
                        <li><strong>And</strong> I should be able to play videos seamlessly</li>
                        <li><strong>And</strong> my progress should be automatically tracked</li>
                    </ul>
                </div>
                
                <div class="validation">
                    <strong>Validation Rules:</strong>
                    <ul>
                        <li>Content access based on enrollment status</li>
                        <li>Sequential access if configured by instructor</li>
                        <li>Video streaming must support multiple formats</li>
                        <li>Progress tracking with timestamp accuracy</li>
                    </ul>
                </div>
            </div>
            
            <div class="user-story">
                <h4>FR-{start_fr+1:03d}: Take Quiz Assessment</h4>
                <p><strong>As a</strong> learner, <strong>I want to</strong> take quizzes and assignments <strong>so that</strong> I can test my understanding and receive feedback.</p>
                
                <div class="acceptance-criteria">
                    <strong>Acceptance Criteria:</strong>
                    <ul>
                        <li><strong>Given</strong> I have completed the required content</li>
                        <li><strong>When</strong> I start a quiz</li>
                        <li><strong>Then</strong> I should see the timer and question count</li>
                        <li><strong>And</strong> I should be able to answer questions within the time limit</li>
                        <li><strong>And</strong> I should receive immediate or delayed feedback</li>
                    </ul>
                </div>
                
                <div class="validation">
                    <strong>Validation Rules:</strong>
                    <ul>
                        <li>Quiz attempt limits enforced (V-004)</li>
                        <li>Time limits strictly enforced</li>
                        <li>Anti-cheating measures implemented</li>
                        <li>Automatic submission at time expiry</li>
                    </ul>
                </div>
            </div>
            
            <div class="user-story">
                <h4>FR-{start_fr+2:03d}: Submit Assignment</h4>
                <p><strong>As a</strong> learner, <strong>I want to</strong> submit assignments <strong>so that</strong> I can complete course requirements and get graded.</p>
                
                <div class="acceptance-criteria">
                    <strong>Acceptance Criteria:</strong>
                    <ul>
                        <li><strong>Given</strong> I have an assignment to complete</li>
                        <li><strong>When</strong> I upload my assignment files</li>
                        <li><strong>Then</strong> the system should validate file types and sizes</li>
                        <li><strong>And</strong> I should receive a submission confirmation</li>
                        <li><strong>And</strong> the instructor should be notified of my submission</li>
                    </ul>
                </div>
                
                <div class="validation">
                    <strong>Validation Rules:</strong>
                    <ul>
                        <li>File type restrictions enforced (V-005)</li>
                        <li>File size limits strictly applied</li>
                        <li>Deadline enforcement with grace period</li>
                        <li>Virus scanning before acceptance</li>
                    </ul>
                </div>
            </div>
        """
    
    else:
        # Generic user stories for other EPICs
        return f"""
            <div class="user-story">
                <h4>FR-{start_fr:03d}: {epic['name']} - Access</h4>
                <p><strong>As a</strong> user, <strong>I want to</strong> access {epic['name'].lower()} features <strong>so that</strong> I can utilize the system effectively.</p>
                
                <div class="acceptance-criteria">
                    <strong>Acceptance Criteria:</strong>
                    <ul>
                        <li><strong>Given</strong> I have appropriate permissions</li>
                        <li><strong>When</strong> I navigate to the {epic['name'].lower()} section</li>
                        <li><strong>Then</strong> I should see all available features</li>
                        <li><strong>And</strong> I should be able to perform authorized actions</li>
                        <li><strong>And</strong> the interface should be responsive and intuitive</li>
                    </ul>
                </div>
                
                <div class="validation">
                    <strong>Validation Rules:</strong>
                    <ul>
                        <li>Role-based access control enforced</li>
                        <li>User permissions validated before action</li>
                        <li>Audit trail maintained for all activities</li>
                        <li>Error handling and user feedback provided</li>
                    </ul>
                </div>
            </div>
            
            <div class="user-story">
                <h4>FR-{start_fr+1:03d}: {epic['name']} - Manage</h4>
                <p><strong>As a</strong> user, <strong>I want to</strong> manage {epic['name'].lower()} data <strong>so that</strong> I can maintain accurate information.</p>
                
                <div class="acceptance-criteria">
                    <strong>Acceptance Criteria:</strong>
                    <ul>
                        <li><strong>Given</strong> I have management permissions</li>
                        <li><strong>When</strong> I create or update records</li>
                        <li><strong>Then</strong> the changes should be saved successfully</li>
                        <li><strong>And</strong> I should receive confirmation of the action</li>
                        <li><strong>And</strong> the data should be immediately available</li>
                    </ul>
                </div>
                
                <div class="validation">
                    <strong>Validation Rules:</strong>
                    <ul>
                        <li>Data validation before saving</li>
                        <li>Mandatory field completion required</li>
                        <li>Duplicate detection for unique fields</li>
                        <li>Version control for audit purposes</li>
                    </ul>
                </div>
            </div>
            
            <div class="user-story">
                <h4>FR-{start_fr+2:03d}: {epic['name']} - Report</h4>
                <p><strong>As a</strong> user, <strong>I want to</strong> generate reports on {epic['name'].lower()} <strong>so that</strong> I can analyze performance and make decisions.</p>
                
                <div class="acceptance-criteria">
                    <strong>Acceptance Criteria:</strong>
                    <ul>
                        <li><strong>Given</strong> I need to analyze {epic['name'].lower()} data</li>
                        <li><strong>When</strong> I generate a report</li>
                        <li><strong>Then</strong> I should see relevant metrics and data</li>
                        <li><strong>And</strong> I should be able to export the report</li>
                        <li><strong>And</strong> the data should be accurate and up-to-date</li>
                    </ul>
                </div>
                
                <div class="validation">
                    <strong>Validation Rules:</strong>
                    <ul>
                        <li>Real-time data accuracy</li>
                        <li>Export format validation</li>
                        <li>Access control for sensitive data</li>
                        <li>Performance optimization for large datasets</li>
                    </ul>
                </div>
            </div>
        """

def generate_user_stories_for_epic(epic, start_fr):
    """Generate detailed user stories with acceptance criteria for an EPIC"""
    epic_name = epic['name'].lower()
    
    if "authentication" in epic_name or "user management" in epic_name:
        return f"""
            <div class="user-story">
                <h4>FR-{start_fr:03d}: User Registration</h4>
                <p><strong>As a</strong> new user, <strong>I want to</strong> register for an account <strong>so that</strong> I can access the system features.</p>
                
                <div class="acceptance-criteria">
                    <strong>Acceptance Criteria:</strong>
                    <ul>
                        <li><strong>Given</strong> I am on the registration page</li>
                        <li><strong>When</strong> I enter valid registration details (email, password, confirm password, full name)</li>
                        <li><strong>And</strong> I accept the terms and conditions</li>
                        <li><strong>Then</strong> my account should be created successfully</li>
                        <li><strong>And</strong> I should receive a verification email</li>
                        <li><strong>And</strong> I should be redirected to the email verification page</li>
                    </ul>
                </div>
                
                <div class="validation">
                    <strong>Validation Rules:</strong>
                    <ul>
                        <li>Email must be unique in the system</li>
                        <li>Password must meet complexity requirements (V-002)</li>
                        <li>Full name must be 2-50 characters</li>
                        <li>Terms acceptance is mandatory</li>
                        <li>Email verification required within 24 hours</li>
                    </ul>
                </div>
            </div>
            
            <div class="user-story">
                <h4>FR-{start_fr+1:03d}: User Login</h4>
                <p><strong>As a</strong> registered user, <strong>I want to</strong> login to my account <strong>so that</strong> I can access my personalized dashboard.</p>
                
                <div class="acceptance-criteria">
                    <strong>Acceptance Criteria:</strong>
                    <ul>
                        <li><strong>Given</strong> I am on the login page</li>
                        <li><strong>When</strong> I enter my valid email and password</li>
                        <li><strong>Then</strong> I should be authenticated successfully</li>
                        <li><strong>And</strong> I should be redirected to my dashboard</li>
                        <li><strong>And</strong> my session should be maintained for 24 hours</li>
                    </ul>
                </div>
                
                <div class="validation">
                    <strong>Validation Rules:</strong>
                    <ul>
                        <li>Email format validation (V-001)</li>
                        <li>Account must be verified and active</li>
                        <li>Maximum 3 failed login attempts before lockout</li>
                        <li>Password reset option available after lockout</li>
                        <li>Session timeout after 30 minutes of inactivity</li>
                    </ul>
                </div>
            </div>
            
            <div class="user-story">
                <h4>FR-{start_fr+2:03d}: Password Reset</h4>
                <p><strong>As a</strong> user who forgot their password, <strong>I want to</strong> reset my password <strong>so that</strong> I can regain access to my account.</p>
                
                <div class="acceptance-criteria">
                    <strong>Acceptance Criteria:</strong>
                    <ul>
                        <li><strong>Given</strong> I am on the forgot password page</li>
                        <li><strong>When</strong> I enter my registered email address</li>
                        <li><strong>Then</strong> I should receive a password reset link via email</li>
                        <li><strong>And</strong> the reset link should be valid for 2 hours</li>
                        <li><strong>And</strong> I should be able to set a new password</li>
                    </ul>
                </div>
                
                <div class="validation">
                    <strong>Validation Rules:</strong>
                    <ul>
                        <li>Email must exist in the system</li>
                        <li>Reset token must be unique and secure</li>
                        <li>New password must meet complexity requirements</li>
                        <li>Old password should be invalidated immediately</li>
                        <li>User must re-login after password reset</li>
                    </ul>
                </div>
            </div>
        """
    
    elif "product" in epic_name or "catalog" in epic_name:
        return f"""
            <div class="user-story">
                <h4>FR-{start_fr:03d}: Product Search</h4>
                <p><strong>As a</strong> customer, <strong>I want to</strong> search for products <strong>so that</strong> I can find items I want to purchase.</p>
                
                <div class="acceptance-criteria">
                    <strong>Acceptance Criteria:</strong>
                    <ul>
                        <li><strong>Given</strong> I am on the product catalog page</li>
                        <li><strong>When</strong> I enter search keywords in the search box</li>
                        <li><strong>Then</strong> I should see relevant products displayed</li>
                        <li><strong>And</strong> results should be sorted by relevance</li>
                        <li><strong>And</strong> I should see product images, prices, and ratings</li>
                    </ul>
                </div>
                
                <div class="validation">
                    <strong>Validation Rules:</strong>
                    <ul>
                        <li>Search query minimum 2 characters</li>
                        <li>Results limited to 50 items per page</li>
                        <li>Search performance must be under 2 seconds</li>
                        <li>Auto-suggestions for misspelled words</li>
                        <li>Filter options for price, category, brand</li>
                    </ul>
                </div>
            </div>
            
            <div class="user-story">
                <h4>FR-{start_fr+1:03d}: Product Details View</h4>
                <p><strong>As a</strong> customer, <strong>I want to</strong> view detailed product information <strong>so that</strong> I can make informed purchasing decisions.</p>
                
                <div class="acceptance-criteria">
                    <strong>Acceptance Criteria:</strong>
                    <ul>
                        <li><strong>Given</strong> I click on a product from search results</li>
                        <li><strong>When</strong> the product details page loads</li>
                        <li><strong>Then</strong> I should see comprehensive product information</li>
                        <li><strong>And</strong> I should see multiple product images</li>
                        <li><strong>And</strong> I should see customer reviews and ratings</li>
                    </ul>
                </div>
                
                <div class="validation">
                    <strong>Validation Rules:</strong>
                    <ul>
                        <li>Product must be active and available</li>
                        <li>Price display with currency formatting</li>
                        <li>Stock availability status</li>
                        <li>Image zoom functionality</li>
                        <li>Related products suggestions</li>
                    </ul>
                </div>
            </div>
            
            <div class="user-story">
                <h4>FR-{start_fr+2:03d}: Add to Cart</h4>
                <p><strong>As a</strong> customer, <strong>I want to</strong> add products to my shopping cart <strong>so that</strong> I can purchase multiple items together.</p>
                
                <div class="acceptance-criteria">
                    <strong>Acceptance Criteria:</strong>
                    <ul>
                        <li><strong>Given</strong> I am viewing a product details page</li>
                        <li><strong>When</strong> I select quantity and click "Add to Cart"</li>
                        <li><strong>Then</strong> the product should be added to my cart</li>
                        <li><strong>And</strong> I should see cart count updated</li>
                        <li><strong>And</strong> I should see a confirmation message</li>
                    </ul>
                </div>
                
                <div class="validation">
                    <strong>Validation Rules:</strong>
                    <ul>
                        <li>Quantity must be positive integer</li>
                        <li>Cannot exceed available stock</li>
                        <li>Cart persistence across sessions</li>
                        <li>Maximum 10 items per product in cart</li>
                        <li>Real-time inventory checking</li>
                    </ul>
                </div>
            </div>
        """
    
    else:
        # Generic user stories for other EPICs
        return f"""
            <div class="user-story">
                <h4>FR-{start_fr:03d}: {epic['name']} - Create</h4>
                <p><strong>As a</strong> user, <strong>I want to</strong> create new {epic['name'].lower()} records <strong>so that</strong> I can manage my business data effectively.</p>
                
                <div class="acceptance-criteria">
                    <strong>Acceptance Criteria:</strong>
                    <ul>
                        <li><strong>Given</strong> I have the necessary permissions</li>
                        <li><strong>When</strong> I fill out the creation form with valid data</li>
                        <li><strong>Then</strong> the record should be saved successfully</li>
                        <li><strong>And</strong> I should receive a confirmation message</li>
                        <li><strong>And</strong> the record should appear in the list view</li>
                    </ul>
                </div>
                
                <div class="validation">
                    <strong>Validation Rules:</strong>
                    <ul>
                        <li>All mandatory fields must be completed</li>
                        <li>Data format validation for each field type</li>
                        <li>Duplicate checking for unique fields</li>
                        <li>Business rule validation</li>
                        <li>User authorization verification</li>
                    </ul>
                </div>
            </div>
            
            <div class="user-story">
                <h4>FR-{start_fr+1:03d}: {epic['name']} - Update</h4>
                <p><strong>As a</strong> user, <strong>I want to</strong> edit existing {epic['name'].lower()} records <strong>so that</strong> I can keep information current and accurate.</p>
                
                <div class="acceptance-criteria">
                    <strong>Acceptance Criteria:</strong>
                    <ul>
                        <li><strong>Given</strong> I have edit permissions for the record</li>
                        <li><strong>When</strong> I modify fields and save changes</li>
                        <li><strong>Then</strong> the record should be updated successfully</li>
                        <li><strong>And</strong> I should see the updated information reflected</li>
                        <li><strong>And</strong> audit trail should capture the changes</li>
                    </ul>
                </div>
                
                <div class="validation">
                    <strong>Validation Rules:</strong>
                    <ul>
                        <li>Record must exist and be editable</li>
                        <li>Concurrent edit conflict detection</li>
                        <li>Field-level validation on changes</li>
                        <li>Version control for tracking changes</li>
                        <li>Rollback capability for critical errors</li>
                    </ul>
                </div>
            </div>
            
            <div class="user-story">
                <h4>FR-{start_fr+2:03d}: {epic['name']} - View/Search</h4>
                <p><strong>As a</strong> user, <strong>I want to</strong> search and view {epic['name'].lower()} records <strong>so that</strong> I can find and access relevant information quickly.</p>
                
                <div class="acceptance-criteria">
                    <strong>Acceptance Criteria:</strong>
                    <ul>
                        <li><strong>Given</strong> I am on the {epic['name'].lower()} list page</li>
                        <li><strong>When</strong> I use search filters or keywords</li>
                        <li><strong>Then</strong> I should see matching records displayed</li>
                        <li><strong>And</strong> results should be paginated for performance</li>
                        <li><strong>And</strong> I should be able to sort by different columns</li>
                    </ul>
                </div>
                
                <div class="validation">
                    <strong>Validation Rules:</strong>
                    <ul>
                        <li>Search performance under 3 seconds</li>
                        <li>Pagination with configurable page size</li>
                        <li>Role-based data visibility</li>
                        <li>Export functionality for search results</li>
                        <li>Advanced filtering options</li>
                    </ul>
                </div>
            </div>
        """

def generate_user_stories_for_epic(epic, start_fr):
    """Generate user stories for EPICs that don't have specific domain logic"""
    epic_name = epic['name']
    
    return f"""
        <div class="user-story">
            <h4>FR-{start_fr:03d}: Access {epic_name}</h4>
            <p><strong>As a</strong> user, <strong>I want to</strong> access {epic_name.lower()} features <strong>so that</strong> I can utilize the system effectively.</p>
            
            <div class="acceptance-criteria">
                <strong>Acceptance Criteria:</strong>
                <ul>
                    <li><strong>Given</strong> I have appropriate permissions</li>
                    <li><strong>When</strong> I navigate to the {epic_name.lower()} section</li>
                    <li><strong>Then</strong> I should see all available features</li>
                    <li><strong>And</strong> I should be able to perform authorized actions</li>
                </ul>
            </div>
        </div>
        
        <div class="user-story">
            <h4>FR-{start_fr+1:03d}: Manage {epic_name}</h4>
            <p><strong>As a</strong> user, <strong>I want to</strong> manage {epic_name.lower()} data <strong>so that</strong> I can maintain accurate information.</p>
            
            <div class="acceptance-criteria">
                <strong>Acceptance Criteria:</strong>
                <ul>
                    <li><strong>Given</strong> I have management permissions</li>
                    <li><strong>When</strong> I create or update records</li>
                    <li><strong>Then</strong> the changes should be saved successfully</li>
                    <li><strong>And</strong> I should receive confirmation</li>
                </ul>
            </div>
        </div>
        
        <div class="user-story">
            <h4>FR-{start_fr+2:03d}: Report on {epic_name}</h4>
            <p><strong>As a</strong> user, <strong>I want to</strong> generate reports on {epic_name.lower()} <strong>so that</strong> I can analyze performance.</p>
            
            <div class="acceptance-criteria">
                <strong>Acceptance Criteria:</strong>
                <ul>
                    <li><strong>Given</strong> I need to analyze data</li>
                    <li><strong>When</strong> I generate a report</li>
                    <li><strong>Then</strong> I should see relevant metrics</li>
                    <li><strong>And</strong> I should be able to export the report</li>
                </ul>
            </div>
        </div>
    """

if __name__ == "__main__":
    print("🚀 Starting Comprehensive FRD Server...")
    uvicorn.run(app, host="0.0.0.0", port=8003, reload=False)