# Customer Request Manager (CRM) — Centralized Compliance Request Tracking

**A unified tenant portal for managing customer compliance and sustainability requests**

---

## Revision History

| Revision | Date | Created By | Changes |
|----------|------|------------|---------|
| R1 | 11/09/2025 | Abhinav R Bharadwaj | Planning Strategy for Customer Request Manager (CRM) |
| R2 | 12/11/2025 | Copilot Agent | Created comprehensive design document from R1 planning artifacts with role-based access and enhanced features |

---

## 1. Summary

The Customer Request Manager (CRM) is a centralized platform for tracking and managing customer compliance and sustainability requests within the Acquis Compliance Platform. It replaces manual tracking methods (email, Excel) with a structured system that provides role-based visibility and ownership. Managers can create, assign, cancel, and monitor all requests, while users focus on executing assigned tasks. The system provides real-time dashboards with KPIs, regulatory heat maps for resource optimization, comprehensive audit trails, and automated business rule enforcement.

**Key Outcomes:**
- Centralized request tracking replacing manual methods
- Role-based access control (Managers vs Users)
- Real-time dashboards with KPIs and regulatory heat maps
- Resource optimization through demand analytics
- Automated business rule enforcement (mandatory cancellation reasons, overdue flagging)
- Comprehensive audit logging for all actions
- File upload/management with Azure Blob Storage integration
- Export capabilities for reporting and compliance

**Recommended Next Steps:**
1. Complete R1 development and deploy to staging
2. Conduct user acceptance testing with pilot customers
3. Validate regulatory heat map accuracy with compliance team
4. Plan R2 enhancements: advanced workflows, notifications, integrations
5. Establish monitoring and SLA tracking

---

## 2. Overview

### 2.1 Purpose

The CRM tool addresses the critical need for organized tracking of customer compliance and sustainability requests. Currently, many organizations rely on manual methods (spreadsheets, email threads) which lack centralization, accountability, and real-time visibility. The CRM provides a structured system with role-based access where managers can oversee all requests and users can focus on their assigned tasks, ensuring clear ownership, efficient resource allocation, and complete audit trails.

### 2.2 Scope

**In Scope:**
- Role-based access control (Manager and User roles)
- Request creation and assignment by managers
- Request lifecycle management (create, update, cancel)
- Soft deletion with mandatory cancellation reasons
- File upload and attachment management
- Summary dashboard with KPIs and visualizations
- **All Requests view (Manager-only)** with filtering and search
- **My Tasks view** for assigned requests (All users)
- Regulatory heat map for resource planning and optimization
- Overdue request flagging and prioritization
- Automated business rule enforcement
- Export functionality (CSV/Excel)
- Audit logging for all actions
- Multi-tenant data isolation

**Out of Scope (Future Releases):**
- Email notifications for assignments/updates
- Integration with external systems (CRM, ticketing)
- Advanced workflow automation
- Custom fields and request templates
- SLA tracking and alerting
- Mobile application
- External customer portal access

### 2.3 Goals & Success Metrics

**Goals:**
1. Reduce request tracking overhead by 60% compared to manual methods
2. Improve request resolution time by providing clear ownership and visibility
3. Ensure 100% audit trail coverage for compliance requirements
4. Support 500+ concurrent users per tenant
5. Achieve <2 second page load times for all views

**Success Metrics:**
- Average request resolution time: < 14 days
- User adoption rate: ≥ 80% of tenant users actively using CRM
- Request completion rate: ≥ 90% of requests closed within deadline
- System availability: ≥ 99.5%
- Data accuracy: Zero cross-tenant data leakage incidents

---

## 3. Key Definitions

| Term | Definition |
|------|------------|
| **CRM** | Customer Request Manager - the compliance request tracking system |
| **Request** | A customer-submitted compliance or sustainability inquiry/requirement |
| **Tenant** | Individual customer organization in the multi-tenant SaaS platform |
| **Manager** | User with full access to create, assign, view all requests, and access analytics |
| **User** | User with access to view and work on assigned requests only (My Tasks) |
| **Assignee** | Tenant user responsible for resolving a request |
| **Soft Delete** | Marking request as cancelled while preserving data for audit |
| **Request Type** | Category of request (Declaration, Clarification, Other) |
| **Regulation** | Specific compliance regulation (RoHS, REACH, TSCA PBT, Prop 65, Conflict Minerals, FMD) |
| **Submitted Via** | Channel through which request was received (Email, Phone, Portal, Meeting) |
| **KPI** | Key Performance Indicator - metrics for measuring system performance |
| **Heat Map** | Visual representation of regulatory request frequency for resource planning |
| **Azure Blob Storage** | Cloud storage service for file attachments (uflpa container) |
| **Overdue Request** | Request past its deadline, automatically flagged for prioritization |

---

## 4. Key Features & Business Rules

### 4.1 Centralized Request Tracking
- All customer requests stored in one centralized system, replacing manual tracking via email or Excel
- **All Requests** page where managers can view, filter, and manage every request
- Complete visibility of request lifecycle from creation to closure

### 4.2 Enhanced Dashboard and Visibility
- Summary Dashboard delivers **key metrics** for instant insight:
  - Total Requests
  - Average Resolve Time
  - Open vs Closed breakdown
  - Request type distribution
- Visual charts:
  - **Donut Chart:** Request completion status (Open, In Progress, Resolved, Closed, On Hold)
  - **Line Graph:** Trends in request volumes over time with Yearly/Monthly filters
  - **Bar Chart:** Types of requests (Declaration, Clarification, Other)
  - **Regulatory Heat Map:** Frequency of requests by regulation, color-coded monthly for resource planning

### 4.3 Request Ownership and Task Management
- Each request is assigned to a responsible user
- **My Tasks** tab enables users to see requests assigned to them
- Users can export their workload for reporting
- Ownership, deadlines, and status kept visible for both users and managers

### 4.4 Automation and Reporting
- Automatic logging of all actions and status changes for traceability
- Export features for requests and assigned tasks support compliance reporting and analytics
- Completion status updates enforced automatically
- Business rules (overdue flagging, required cancellation reasons) automated

### 4.5 Resource Optimization
- **Regulatory demand heat maps** help optimize team resources
- Shows monthly volume for each regulation (RoHS, REACH, TSCA PBT, Prop 65, Conflict Minerals, FMD)
- Color-coded visualization for quick identification of high-demand areas
- Insights provided through dashboard visualizations and downloadable reports

### 4.6 Smart Request Form Handling
- All key fields managed by dropdowns, calendar pickers, and validation logic
- Validations ensure:
  - Mandatory fields are completed
  - Date constraints are respected
  - Cancellation reasons are entered when required
- Form supports adding, editing, and cancelling requests with mandatory justification

### 4.7 Business Rule Enforcement
- **Cancellation must include a reason** (justification required)
- **Overdue requests flagged** for prioritization
- **Completion status auto-updated** when requests are resolved or closed
- **Heat map generation automated** by system logic
- **Role-based access enforced** at all layers

### 4.8 Data Inputs and Outputs
**Inputs:**
- Customer name
- Request type (Declaration, Clarification, Other)
- Submission source
- Regulation (RoHS, REACH, TSCA PBT, Prop 65, Conflict Minerals, FMD)
- Assigned manager
- Important dates (request date, deadline)
- Comments and attachments

**Outputs:**
- Request status and completion time
- Visual charts and analytics
- Regulatory heat maps
- Exported files for reporting
- Audit trails

---

## 5. Proposed Design (High-Level)

### 5.1 User Flow: Creating and Resolving a Request (Manager)

```
Manager logs into CRM
    ↓
Navigate to Summary Dashboard (landing page)
    ↓
View KPIs, charts, and regulatory heat map
    ↓
Click "All Requests" to see full list (Manager-only access)
    ↓
Click "Add Request" button
    ↓
Fill Request Form (customer, type, regulations, assignee, deadline)
    ↓
System validates mandatory fields and date constraints
    ↓
Upload attachments (optional)
    ↓
Save request → System generates Request ID
    ↓
Request appears in "All Requests" and assignee's "My Tasks"
    ↓
Assignee (User) updates status, adds comments, uploads files
    ↓
Request progresses: Open → In Progress → Resolved → Closed
    ↓
System auto-flags overdue requests
    ↓
All actions logged in audit trail
```

### 5.2 User Flow: User Working on Assigned Task

```
User logs into CRM
    ↓
Navigate to Summary Dashboard (personal metrics visible)
    ↓
View My Open/Closed Tasks, Overdue Tasks, Personal completion trends
    ↓
Click "My Tasks" tab
    ↓
View only requests assigned to them
    ↓
Select a request to work on
    ↓
Update status (Open → In Progress → Resolved)
    ↓
Add comments or upload files
    ↓
Export My Tasks for personal reporting
    ↓
All actions logged in audit trail
```

### 5.3 User Flow: Cancelling a Request (Manager)

```
Manager navigates to "All Requests"
    ↓
Select one or more requests (checkbox)
    ↓
Click "Cancel" action button
    ↓
Popup appears: "Cancel Request"
    ↓
Enter mandatory cancellation reason
    ↓
Click "Confirm Cancel" or "Keep Requests"
    ↓
If confirmed: Requests marked as cancelled (soft delete)
    ↓
Audit log records cancellation reason and user
```

### 5.4 Component Responsibilities

| Component | Responsibility |
|-----------|---------------|
| **Summary Dashboard** | Display KPIs, charts, regulatory heat map, and personal task summaries; Role-based views (Managers see all metrics, Users see personal metrics) |
| **All Requests View (Manager-only)** | Comprehensive table of all tenant requests with filters, search, and actions; Create new requests, cancel requests |
| **Request Form** | Intake new requests with validation, mandatory field checks, date constraints, and file uploads |
| **My Tasks View (All users)** | Personalized view of requests assigned to logged-in user; Update status, add comments, upload files, export tasks |
| **Cancel Request Popup** | Handle soft deletion with mandatory reason capture (minimum 10 characters) |
| **Regulatory Heat Map** | Visual representation of request frequency by regulation, color-coded monthly for resource planning |
| **Export Service** | Generate CSV/Excel exports of request data; Role-based filtering (Managers: all requests, Users: my tasks) |
| **Audit Logger** | Record all user actions with timestamp, user, role, and details |
| **File Storage Service** | Manage file uploads to Azure Blob Storage (uflpa container) |
| **Business Rule Engine** | Enforce overdue flagging, mandatory cancellation reasons, status transitions, role-based access |

### 4.4 Data Flow

```
[User Action] → [Frontend ReactJS Component]
                      ↓
              [API Request to Fastify Backend]
                      ↓
              [Authentication & Authorization]
                      ↓
              [Business Logic Layer]
                      ↓
         ┌────────────┴────────────┐
         ↓                         ↓
   [MongoDB]                 [Azure Blob Storage]
   (Request Data)             (File Attachments)
         ↓                         ↓
   [Audit Log Entry]          [File Metadata]
         ↓                         ↓
         └────────────┬────────────┘
                      ↓
              [Response to Frontend]
                      ↓
              [UI Update with New Data]
```

---

## 5. System Architecture

### 5.1 Logical Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    Frontend Layer (React)                     │
│  ┌────────────┐  ┌────────────┐  ┌────────────────┐         │
│  │  Summary   │  │    All     │  │   My Tasks     │         │
│  │ Dashboard  │  │  Requests  │  │     View       │         │
│  │(Role-based)│  │ (Manager)  │  │  (All users)   │         │
│  └────────────┘  └────────────┘  └────────────────┘         │
│  ┌────────────┐  ┌────────────┐  ┌────────────────┐         │
│  │  Request   │  │   Cancel   │  │  FusionCharts  │         │
│  │    Form    │  │   Popup    │  │  + Heat Map    │         │
│  │ (Manager)  │  │ (Manager)  │  │  Visualizations│         │
│  └────────────┘  └────────────┘  └────────────────┘         │
└─────────────────────────┬────────────────────────────────────┘
                          │ REST API (Fastify)
┌─────────────────────────▼────────────────────────────────────┐
│                    Backend Layer (Node.js)                    │
│  ┌────────────┐  ┌────────────┐  ┌────────────────┐         │
│  │  Request   │  │   File     │  │     Audit      │         │
│  │  Service   │  │  Service   │  │    Logger      │         │
│  └────────────┘  └────────────┘  └────────────────┘         │
│  ┌────────────┐  ┌────────────┐  ┌────────────────┐         │
│  │  Export    │  │   Auth +   │  │   Validation   │         │
│  │  Service   │  │   RBAC     │  │    Service     │         │
│  └────────────┘  └────────────┘  └────────────────┘         │
│  ┌────────────┐  ┌────────────┐                             │
│  │  Business  │  │  Heat Map  │                             │
│  │   Rules    │  │  Generator │                             │
│  └────────────┘  └────────────┘                             │
└─────────────────┬───────────────────────┬───────────────────┘
                  │                       │
         ┌────────▼─────────┐    ┌───────▼──────────┐
         │    MongoDB        │    │ Azure Blob       │
         │ (Multi-tenant     │    │ Storage          │
         │  Collections)     │    │ (uflpa container)│
         └───────────────────┘    └──────────────────┘
```

### 5.2 Backend Services

**Fastify Server:**
- REST API endpoints for CRUD operations
- Request validation with mandatory field checks
- Multi-tenant database routing
- JWT authentication and role-based authorization (Manager vs User)
- Error handling and logging

**Request Service:**
- Request lifecycle management (create, update, cancel)
- Status transitions with validation rules
- Assignment management
- Overdue request detection and flagging

**Business Rules Engine:**
- Enforce mandatory cancellation reasons (min 10 characters)
- Auto-flag overdue requests
- Validate status transitions
- Enforce role-based access at service layer

**Heat Map Generator:**
- Calculate monthly request frequency by regulation
- Generate color-coded heat map data
- Aggregate data for resource planning insights

**File Service:**
- File upload to Azure Blob Storage (uflpa container)
- File metadata persistence in MongoDB
- File download and deletion
- File size and type validation

**Export Service:**
- CSV/Excel generation from request data
- Filtered exports based on user selection
- Scheduled export for reporting (future)

**Audit Logger:**
- Capture all user actions (create, update, cancel, export)
- Store user identity, timestamp, action type, and details
- Queryable audit trail for compliance

### 5.3 Frontend Considerations

**React Components:**
- **Summary Dashboard:** KPI cards, donut charts, line charts, bar charts, regulatory heat maps; Role-based views (Managers see all tenant metrics, Users see personal metrics)
- **All Requests Table (Manager-only):** Sortable, filterable, searchable data grid with create, cancel, and export actions
- **Request Form (Manager-only):** Multi-field form with mandatory field validation, date constraints, dropdown selectors, calendar pickers, and file upload
- **My Tasks (All users):** Filtered view of assigned requests with status update, comment, file upload, and export capabilities
- **Cancel Popup (Manager-only):** Modal dialog with mandatory reason input (min 10 characters validation)
- **Regulatory Heat Map:** Color-coded monthly visualization of regulation frequency (RoHS, REACH, TSCA PBT, Prop 65, Conflict Minerals, FMD)

**State Management:**
- React Context API for global state (user session, tenant info, role)
- Role-based rendering and route protection
- Local component state for form inputs and UI interactions
- Ant Design form state management

**Role-Based Access Control (Frontend):**
- Route guards for manager-only pages (All Requests, Request Form)
- Conditional rendering based on user role
- Manager role: Full access to all features
- User role: Access to My Tasks, view personal dashboard metrics

**Performance Optimizations:**
- Pagination for large request lists (20 per page)
- Lazy loading for charts and visualizations
- Debounced search input
- Memoized components for static data
- Heat map data caching (refresh every 5 minutes)

**Visualization:**
- FusionCharts for interactive charts
- Donut chart: Request status distribution (Open, In Progress, Resolved, Closed, On Hold)
- Line chart: Request trends over time with Yearly/Monthly filters
- Bar chart: Request type breakdown (Declaration, Clarification, Other)
- Heat map: Regulatory demand by month, color-coded for quick resource planning

### 5.4 Third-Party Integrations

| Service | Purpose | Configuration |
|---------|---------|---------------|
| **Azure Blob Storage** | File attachment storage | Container: uflpa, Connection string in env vars |
| **MongoDB** | Primary database | Multi-tenant collections, replica set for HA |
| **FusionCharts** | Data visualization | Client-side library, included in React app |
| **Ant Design** | UI component library | v4.x, TypeScript support |

---

## 6. Database Design

### 6.1 Requests Collection Schema

```javascript
{
  _id: ObjectId,                    // Unique request identifier
  requestId: String,                // Human-readable ID (e.g., "CRM-2025-001")
  tenantNumber: String,             // Tenant isolation key
  customer: String,                 // Customer name/company
  submittedVia: String,             // "Email" | "Phone" | "Portal" | "Meeting"
  requestDate: Date,                // Date request was received
  requestType: String,              // "Declaration" | "Clarification" | "Other"
  regulations: [String],            // Array of applicable regulations (RoHS, REACH, TSCA PBT, Prop 65, Conflict Minerals, FMD)
  assignedTo: String,               // User email of assignee
  deadline: Date,                   // Target completion date
  status: String,                   // "Open" | "In Progress" | "Resolved" | "Closed" | "On Hold"
  isOverdue: Boolean,               // Auto-calculated flag for past deadline
  comments: String,                 // Additional notes/context
  attachments: [                    // Array of file metadata
    {
      fileName: String,
      fileUrl: String,              // Azure Blob Storage URL
      uploadedBy: String,           // User email
      uploadedAt: Date,
      fileSize: Number              // Size in bytes
    }
  ],
  cancellationReason: String,       // Required if status is "Cancelled" (min 10 characters)
  cancelledBy: String,              // User who cancelled (must be Manager)
  cancelledAt: Date,                // Cancellation timestamp
  createdBy: String,                // User who created request (Manager)
  createdByRole: String,            // "Manager" | "User"
  createdAt: Date,                  // MongoDB timestamp
  updatedAt: Date,                  // MongoDB timestamp
  lastModifiedBy: String,           // User who last updated
  lastModifiedByRole: String        // "Manager" | "User"
}
```

### 6.2 Audit Logs Collection Schema

```javascript
{
  _id: ObjectId,
  tenantNumber: String,             // Tenant isolation
  requestId: String,                // Related request ID
  userId: String,                   // User who performed action
  userName: String,                 // User display name
  userRole: String,                 // "Manager" | "User"
  action: String,                   // "CREATE" | "UPDATE" | "CANCEL" | "EXPORT" | "UPLOAD" | "STATUS_CHANGE"
  details: Object,                  // Action-specific details
  timestamp: Date,                  // When action occurred
  ipAddress: String,                // User IP (optional)
  userAgent: String                 // Browser info (optional)
}
```

### 6.3 Indexes

```javascript
// Requests collection
db.requests.createIndex({ tenantNumber: 1, requestId: 1 }, { unique: true })
db.requests.createIndex({ tenantNumber: 1, status: 1, requestDate: -1 })
db.requests.createIndex({ tenantNumber: 1, assignedTo: 1, status: 1 })
db.requests.createIndex({ tenantNumber: 1, customer: 1 })
db.requests.createIndex({ tenantNumber: 1, requestType: 1 })
db.requests.createIndex({ tenantNumber: 1, deadline: 1 })
db.requests.createIndex({ tenantNumber: 1, isOverdue: 1, status: 1 })
db.requests.createIndex({ tenantNumber: 1, regulations: 1 })

// Audit logs collection
db.auditLogs.createIndex({ tenantNumber: 1, requestId: 1, timestamp: -1 })
db.auditLogs.createIndex({ tenantNumber: 1, userId: 1, timestamp: -1 })
db.auditLogs.createIndex({ timestamp: -1 })

// TTL index for audit log retention (7 years for compliance)
db.auditLogs.createIndex({ timestamp: 1 }, { expireAfterSeconds: 220752000 })
```

### 6.4 Data Retention Rules

- **Active Requests:** Retained indefinitely
- **Closed Requests:** Retained for 7 years (compliance requirement)
- **Cancelled Requests:** Retained for 7 years (soft delete preserves data)
- **Audit Logs:** Retained for 7 years, then auto-deleted via TTL index
- **File Attachments:** Retained while associated request exists
- **Backup Policy:** Daily MongoDB backups, 30-day retention

---

## 7. API Contracts

### 7.1 Create Request

**Endpoint:** `POST /api/crm/requests`

**Role Required:** Manager

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "customer": "Acme Corporation",
  "submittedVia": "Email",
  "requestDate": "2025-11-10",
  "requestType": "Declaration",
  "regulations": ["REACH", "RoHS"],
  "assignedTo": "john.doe@company.com",
  "deadline": "2025-11-30",
  "comments": "Customer needs full BOM compliance data for Q4 audit"
}
```

**Response:** `201 Created`
```json
{
  "success": true,
  "message": "Request created successfully",
  "data": {
    "requestId": "CRM-2025-001",
    "_id": "673abc123def456789",
    "status": "Open",
    "createdAt": "2025-11-12T10:00:00Z"
  }
}
```

**Validation Rules:**
- `customer`: Required, max 200 characters
- `submittedVia`: Required, must be one of: Email, Phone, Portal, Meeting
- `requestDate`: Required, cannot be future date
- `requestType`: Required, must be one of: Declaration, Clarification, Other
- `regulations`: Required, array with at least one item from: RoHS, REACH, TSCA PBT, Prop 65, Conflict Minerals, FMD
- `assignedTo`: Required, must be valid user email in tenant
- `deadline`: Required, must be after requestDate
- `comments`: Optional, max 2000 characters

**Business Rules:**
- Only Managers can create requests
- System auto-calculates isOverdue flag based on deadline
- Request status defaults to "Open"

**Error Responses:**
- `400 Bad Request` - Validation errors
- `401 Unauthorized` - Invalid token
- `403 Forbidden` - User role is not Manager
- `500 Internal Server Error` - Server error

---

### 7.2 Get All Requests

**Endpoint:** `GET /api/crm/requests`

**Role Required:** Manager

**Query Parameters:**
```
page: number (default: 1)
limit: number (default: 20, max: 100)
status: string (filter by status: Open, In Progress, Resolved, Closed, On Hold)
customer: string (filter by customer name)
requestType: string (filter by type: Declaration, Clarification, Other)
assignedTo: string (filter by assignee email)
isOverdue: boolean (filter overdue requests)
regulations: string (filter by regulation)
search: string (search across customer, requestId, comments)
sortBy: string (default: "requestDate")
sortOrder: "asc" | "desc" (default: "desc")
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "requests": [
      {
        "requestId": "CRM-2025-001",
        "customer": "Acme Corporation",
        "requestType": "Declaration",
        "regulations": ["REACH", "RoHS"],
        "assignedTo": "john.doe@company.com",
        "status": "In Progress",
        "isOverdue": false,
        "requestDate": "2025-11-10",
        "deadline": "2025-11-30",
        "createdAt": "2025-11-12T10:00:00Z"
      }
    ],
    "pagination": {
      "currentPage": 1,
      "totalPages": 5,
      "totalRecords": 95,
      "limit": 20
    }
  }
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid token
- `403 Forbidden` - User role is not Manager
- `500 Internal Server Error` - Server error

---

### 7.3 Get My Tasks

**Endpoint:** `GET /api/crm/my-tasks`

**Role Required:** All users (Manager and User)

**Query Parameters:**
```
page: number (default: 1)
limit: number (default: 20)
status: string (filter by status, default: shows Open + In Progress)
isOverdue: boolean (filter overdue tasks)
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "tasks": [
      {
        "requestId": "CRM-2025-001",
        "customer": "Acme Corporation",
        "requestType": "Compliance Data",
        "status": "In Progress",
        "deadline": "2025-11-30",
        "daysRemaining": 18
      }
    ],
    "summary": {
      "totalAssigned": 12,
      "openCount": 5,
      "inProgressCount": 4,
      "overdueCount": 3
    }
  }
}
```

---

### 7.4 Update Request

**Endpoint:** `PATCH /api/crm/requests/:requestId`

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:** (all fields optional)
```json
{
  "status": "In Progress",
  "comments": "Updated with additional customer clarifications",
  "assignedTo": "jane.smith@company.com",
  "deadline": "2025-12-15"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "Request updated successfully",
  "data": {
    "requestId": "CRM-2025-001",
    "updatedAt": "2025-11-12T11:00:00Z"
  }
}
```

**Status Transition Rules:**
- Open → In Progress, Cancelled
- In Progress → Resolved, Open, Cancelled
- Resolved → Closed, In Progress
- Closed → (terminal state, no transitions)
- Cancelled → (terminal state, no transitions)

---

### 7.5 Cancel Request (Soft Delete)

**Endpoint:** `POST /api/crm/requests/cancel`

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "requestIds": ["CRM-2025-001", "CRM-2025-002"],
  "cancellationReason": "Customer withdrew request due to project delay"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "2 requests cancelled successfully",
  "data": {
    "cancelledCount": 2,
    "cancelledIds": ["CRM-2025-001", "CRM-2025-002"]
  }
}
```

**Validation:**
- `requestIds`: Required, array with at least one valid request ID
- `cancellationReason`: Required, min 10 characters, max 500 characters
- Only Open or In Progress requests can be cancelled

---

### 7.6 Upload File

**Endpoint:** `POST /api/crm/requests/:requestId/files`

**Headers:**
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Request Body:**
```
file: <binary file data>
```

**Response:** `201 Created`
```json
{
  "success": true,
  "message": "File uploaded successfully",
  "data": {
    "fileName": "compliance_report.pdf",
    "fileUrl": "https://storage.azure.com/uflpa/673abc123def456789/compliance_report.pdf",
    "fileSize": 2048576,
    "uploadedAt": "2025-11-12T11:30:00Z"
  }
}
```

**File Constraints:**
- Max file size: 50 MB
- Allowed types: PDF, Excel, Word, Images (JPG, PNG), CSV
- Files stored in Azure Blob Storage (uflpa container)
- File metadata saved in request document

---

### 7.7 Export Requests

**Endpoint:** `POST /api/crm/requests/export`

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "format": "csv",
  "filters": {
    "status": "Open",
    "requestType": "Compliance Data"
  },
  "fields": ["requestId", "customer", "status", "deadline", "assignedTo"]
}
```

**Response:** `200 OK`
```
Content-Type: text/csv
Content-Disposition: attachment; filename="crm_requests_export_2025-11-12.csv"

Request ID,Customer,Status,Deadline,Assigned To
CRM-2025-001,Acme Corporation,Open,2025-11-30,john.doe@company.com
CRM-2025-002,Beta Industries,Open,2025-12-15,jane.smith@company.com
```

**Supported Formats:**
- CSV (comma-separated values)
- Excel (XLSX)

---

### 7.8 Get Dashboard KPIs

**Endpoint:** `GET /api/crm/dashboard/kpis`

**Role Required:** Manager (full tenant metrics), User (personal metrics only)

**Headers:**
```
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "totalRequests": 150,
    "avgResolveTime": 11.5,
    "openRequests": 45,
    "closedRequests": 85,
    "cancelledRequests": 20,
    "overdueRequests": 12,
    "onHoldRequests": 8,
    "statusDistribution": {
      "Open": 45,
      "In Progress": 30,
      "Resolved": 10,
      "Closed": 85,
      "On Hold": 8,
      "Cancelled": 20
    },
    "requestTypeBreakdown": {
      "Declaration": 80,
      "Clarification": 50,
      "Other": 20
    },
    "regulationHeatMap": {
      "monthly": [
        {
          "regulation": "RoHS",
          "data": [12, 15, 18, 20, 22, 25],
          "months": ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar"],
          "colorIntensity": "high"
        },
        {
          "regulation": "REACH",
          "data": [10, 12, 14, 16, 18, 20],
          "months": ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar"],
          "colorIntensity": "high"
        },
        {
          "regulation": "TSCA PBT",
          "data": [5, 6, 7, 8, 9, 10],
          "months": ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar"],
          "colorIntensity": "medium"
        },
        {
          "regulation": "Prop 65",
          "data": [4, 5, 6, 7, 8, 9],
          "months": ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar"],
          "colorIntensity": "medium"
        },
        {
          "regulation": "Conflict Minerals",
          "data": [8, 9, 10, 11, 12, 13],
          "months": ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar"],
          "colorIntensity": "medium"
        },
        {
          "regulation": "FMD",
          "data": [3, 4, 5, 6, 7, 8],
          "months": ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar"],
          "colorIntensity": "low"
        }
      ],
      "totalByRegulation": {
        "RoHS": 112,
        "REACH": 90,
        "TSCA PBT": 45,
        "Prop 65": 39,
        "Conflict Minerals": 63,
        "FMD": 33
      }
    },
    "trendData": {
      "labels": ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar"],
      "datasets": [
        {
          "label": "Requests Created",
          "data": [42, 51, 60, 68, 76, 85]
        },
        {
          "label": "Requests Closed",
          "data": [35, 45, 52, 60, 68, 75]
        }
      ]
    },
    "myTasks": {
      "openCount": 5,
      "inProgressCount": 3,
      "overdueCount": 2,
      "completedThisMonth": 8,
      "personalCompletionTrend": [5, 6, 7, 8, 9, 8]
    }
  }
}
```

**Note:** 
- Managers receive full tenant metrics including all requests and regulatory heat maps
- Users receive only personal task metrics (myTasks section)

---

### 7.9 Authentication Model

**JWT Token Structure:**
```javascript
{
  emailAddress: "user@company.com",
  tenantNumber: "TENANT001",
  userId: "user123",
  userName: "John Doe",
  role: "Manager" | "User",
  iat: 1699876543,
  exp: 1699905343
}
```

**Authorization Rules:**
- **Manager Role:** Full access to all CRM features
  - Create, assign, cancel requests
  - View All Requests
  - Access full dashboard with tenant-wide metrics
  - Export all requests
- **User Role:** Limited access
  - View and update only assigned requests (My Tasks)
  - View personal metrics on dashboard
  - Export own tasks
  - Cannot create or cancel requests
- Users can only see data from their own tenant
- Tenant isolation enforced at database query level
- Role verification enforced at API, service, and database layers

---

## 8. Failure Scenarios & Mitigations

### 8.1 Unauthorized Access to Manager-Only Features

**Scenario:** User role attempts to access All Requests page or create a request

**Impact:** Potential security breach, unauthorized data access

**Mitigation:**
- **Frontend Route Guards:** Redirect users to My Tasks if they attempt to access All Requests
- **API Authorization:** Return 403 Forbidden if User role calls Manager-only endpoints
- **Role Verification:** Check JWT token role on every request
- **Audit Trail:** Log all unauthorized access attempts
- **UI Hiding:** Hide Create Request and Cancel buttons for User role

**Detection:** Monitor 403 Forbidden responses; audit log analysis

---

### 8.2 Overdue Request Not Flagged

**Scenario:** Request passes deadline but isOverdue flag not updated

**Impact:** Missed SLAs, customer dissatisfaction, resource misallocation

**Mitigation:**
- **Scheduled Job:** Daily cron job to update isOverdue flags for all requests past deadline
- **Real-time Check:** Calculate isOverdue on-the-fly during API requests
- **Dashboard Alert:** Highlight overdue count prominently on dashboard
- **Email Notifications:** Send alerts for overdue requests (R2 feature)
- **Automated Escalation:** Auto-assign priority to overdue requests (future)

**Detection:** Dashboard shows overdue count; automated job logs

---

### 8.3 Duplicate Request Creation

**Scenario:** Manager attempts to create a request that already exists

**Impact:** Redundant work, data confusion, inflated KPIs

**Mitigation:**
- **Warning Message:** Show "Similar request may exist" with list of matching requests
- **User Confirmation:** Allow manager to review and confirm if truly different
- **Audit Trail:** Log all duplicate creation attempts for analysis

**Detection:** Backend validation during request creation API call

---

### 8.2 File Upload Failure

**Scenario:** File upload to Azure Blob Storage fails due to network issues or storage unavailability

**Impact:** User cannot attach supporting documents to request

**Mitigation:**
- **Retry Logic:** 3 retry attempts with exponential backoff (2s, 4s, 8s)
- **Error Handling:** Return clear error message to user
- **Partial Save:** Save request metadata even if file upload fails
- **Manual Retry:** Allow user to re-upload file later via request detail page
- **Monitoring:** Alert on high file upload failure rate

**Detection:** Azure Blob Storage SDK throws exception; monitored via application logs

---

### 8.3 Database Connection Failure

**Scenario:** MongoDB becomes unavailable or connection times out

**Impact:** Cannot create, update, or retrieve requests

**Mitigation:**
- **Connection Pool:** Maintain pool of database connections for resilience
- **Retry Logic:** 3 retry attempts for transient failures
- **Circuit Breaker:** Temporarily disable requests after repeated failures to prevent cascading
- **Error Response:** Return 503 Service Unavailable to client
- **Health Check:** Periodic health check endpoint for monitoring
- **Backup Connection:** Secondary MongoDB replica for failover

**Detection:** MongoDB driver throws connection errors; health check fails

---

### 8.4 Concurrent Update Conflicts

**Scenario:** Two users update the same request simultaneously

**Impact:** One user's changes may overwrite another's (lost update problem)

**Mitigation:**
- **Optimistic Locking:** Use version field or lastModifiedAt timestamp
- **Conflict Detection:** Compare lastModifiedAt before saving update
- **User Notification:** "Request was modified by another user. Please refresh and try again."
- **Audit Trail:** Log all updates with user and timestamp
- **Future Enhancement:** Real-time collaboration with conflict resolution UI

**Detection:** Compare lastModifiedAt during update; detect version mismatch

---

### 8.5 Unauthorized Access Attempt

**Scenario:** User attempts to access requests from different tenant

**Impact:** Data breach, cross-tenant data leakage

**Mitigation:**
- **Multi-Layer Filtering:** Enforce tenant isolation at API, service, and database layers
- **JWT Validation:** Extract tenantNumber from token and validate on every request
- **Database Queries:** Always include tenantNumber filter in MongoDB queries
- **Integration Tests:** Comprehensive tests for tenant isolation
- **Audit Logging:** Log all access attempts with tenant info for forensics
- **Monitoring:** Alert on any cross-tenant access attempts

**Detection:** Automated tests; security scans; audit log analysis

---

### 8.6 Data Export Performance Degradation

**Scenario:** Export request for large dataset (10,000+ records) causes timeout or high memory usage

**Impact:** Export fails, poor user experience, potential server crash

**Mitigation:**
- **Pagination:** Process exports in batches (1,000 records per batch)
- **Streaming:** Stream data to response instead of loading all into memory
- **Timeout Limits:** Set reasonable timeout (60 seconds) for export operations
- **Async Export:** For very large datasets, generate file asynchronously and email download link (future)
- **Rate Limiting:** Limit export frequency per user (max 5 per hour)
- **Caching:** Cache common export queries for 5 minutes

**Detection:** Monitor export API response times and memory usage

---

### 8.7 Deadline Tracking Accuracy

**Scenario:** System does not accurately track or alert on approaching/overdue deadlines

**Impact:** Missed SLAs, customer dissatisfaction, compliance issues

**Mitigation:**
- **Deadline Calculation:** Calculate daysRemaining dynamically in API responses
- **Visual Indicators:** Show red/yellow/green status based on deadline proximity
- **Dashboard Alerts:** Highlight overdue tasks on dashboard
- **Notification System:** Implement email/in-app notifications for approaching deadlines (future)
- **SLA Reports:** Generate weekly reports on deadline performance
- **Escalation:** Automatic escalation for overdue high-priority requests (future)

**Detection:** Dashboard KPIs show overdue count; user reports missed deadlines

---

## 9. Security & Privacy

### 9.1 Threat Model Highlights

| Threat | Impact | Mitigation |
|--------|--------|------------|
| **JWT Token Theft** | Attacker accesses tenant requests | Short token expiry (8 hours), HTTPS only, secure storage |
| **Cross-Tenant Data Leakage** | User sees another tenant's requests | Multi-layer tenant filtering, comprehensive testing |
| **XSS in Request Comments** | Malicious script execution | Sanitize all user input, CSP headers |
| **SQL/NoSQL Injection** | Attacker accesses unauthorized data | Use ODM (Mongoose), parameterized queries, input validation |
| **File Upload Malware** | Virus/malware uploaded to storage | File type validation, size limits, antivirus scanning (future) |
| **Unauthorized File Access** | User downloads files from other tenant's requests | Generate signed URLs with expiry, validate tenant before serving |
| **Brute Force Login** | Attacker guesses user credentials | Rate limiting, account lockout, 2FA (future) |
| **CSRF Attacks** | Attacker performs actions on behalf of user | CSRF tokens, SameSite cookies |

---

### 9.2 Authentication & Authorization

**Authentication:**
- JWT token required for all API endpoints
- Token includes user email, tenant number, and role
- Token validated on every request using shared secret
- Token expiration: 8 hours (configurable)

**Authorization:**
- Role-agnostic: All tenant users have equal permissions
- Tenant isolation: Users can only access data from their tenant
- Database queries always filtered by tenantNumber from JWT
- No admin override capability to access other tenant data

**Session Management:**
- Stateless authentication via JWT
- No server-side session storage required
- Token refresh mechanism (future enhancement)

---

### 9.3 Data Encryption

**In Transit:**
- All API traffic over HTTPS (TLS 1.2+)
- Azure Blob Storage connections use HTTPS
- MongoDB connections use TLS

**At Rest:**
- MongoDB data encrypted at rest via Azure encryption
- Azure Blob Storage encrypted at rest (server-side encryption)
- Sensitive fields (cancellation reasons, comments) treated as confidential

**File Storage Security:**
- Files stored in Azure Blob Storage with private access level
- Signed URLs with expiration for file downloads
- No public URL access to files

---

### 9.4 Input Validation & Sanitization

**Frontend Validation:**
- Required field validation
- Email format validation
- Date range validation (requestDate ≤ today, deadline ≥ requestDate)
- Max length validation for text fields
- Ant Design form validation rules

**Backend Validation:**
- Schema validation using Joi or similar library
- SQL/NoSQL injection prevention via Mongoose ODM
- XSS prevention: sanitize all user input before storing
- File upload validation: type, size, extension
- Duplicate detection before saving

---

### 9.5 Audit Logging & Compliance

**Audit Trail Coverage:**
- All CRUD operations on requests
- File uploads and downloads
- Export operations
- User login/logout (future)
- Failed authorization attempts

**Audit Log Contents:**
- User identity (email, name, tenant)
- Action type (CREATE, UPDATE, CANCEL, etc.)
- Timestamp (ISO 8601 format)
- IP address (optional)
- Request details (before and after state for updates)

**Compliance Requirements:**
- 7-year retention for audit logs (SOX, GDPR requirements)
- Immutable audit logs (append-only collection)
- Encrypted storage for sensitive audit data
- Regular audit log reviews for anomaly detection

---

### 9.6 Secrets Management

**Environment Variables:**
- MongoDB connection string stored in Azure Key Vault
- Azure Blob Storage connection string in Key Vault
- JWT signing secret rotated quarterly
- No secrets in code or Git repository

**Access Control:**
- Key Vault access restricted to production service principal
- Developers use separate dev/staging secrets
- Production secrets never shared via Slack/email
- Secrets rotation procedure documented

---

## 10. Non-Functional Requirements

### 10.1 Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Page Load Time** | < 2 seconds | Time to render Summary Dashboard |
| **API Response Time** | < 500ms (p95) | Backend API latency |
| **Database Query Time** | < 100ms (p95) | MongoDB query execution |
| **File Upload Time** | < 5 seconds for 10MB file | Upload to Azure Blob Storage |
| **Export Generation Time** | < 30 seconds for 1,000 records | CSV/Excel export |
| **Dashboard Chart Rendering** | < 1 second | FusionCharts visualization load time |

---

### 10.2 Scalability Plan

**Current Scale (R1):**
- 500 concurrent users per tenant
- 10,000 requests per tenant
- 50 MB max file size per attachment
- 1 GB total storage per tenant

**Future Scale (R2 - 12 months):**
- 2,000 concurrent users per tenant
- 100,000 requests per tenant
- 100 MB max file size
- 10 GB total storage per tenant

**Scaling Strategies:**
- **Horizontal Backend Scaling:** Add more Fastify instances behind load balancer
- **Database Sharding:** Separate high-volume tenants to dedicated MongoDB instances
- **Storage Scaling:** Azure Blob Storage scales automatically
- **CDN Integration:** Serve static assets via CDN for faster load times
- **Caching:** Redis cache for frequently accessed data (dashboard KPIs)

---

### 10.3 Monitoring & Alerting Plan

**Key Metrics to Monitor:**

1. **Application Performance:**
   - API response times (p50, p95, p99)
   - Page load times
   - Database query performance
   - File upload success/failure rate

2. **Business Metrics:**
   - Requests created per day
   - Average resolution time
   - Overdue request count
   - User adoption rate (active users per tenant)

3. **Infrastructure:**
   - MongoDB connection pool utilization
   - Azure Blob Storage throughput
   - Backend CPU/memory usage
   - Network latency

4. **Error Metrics:**
   - API error rate (4xx, 5xx)
   - Database connection failures
   - File upload failures
   - Authentication failures

**Alerting Rules:**
- API error rate > 5% for 5 minutes
- API response time p95 > 2 seconds for 5 minutes
- Database connection failure
- File upload failure rate > 10%
- Overdue request count > 50 for any tenant
- Backend memory usage > 80% for 10 minutes

**Monitoring Tools:**
- Application Insights for metrics and distributed tracing
- Azure Monitor for infrastructure metrics
- Grafana dashboards for real-time visualization
- PagerDuty for on-call alerting

---

### 10.4 SLA Commitments

| Service Component | Availability SLA | Recovery Time Objective (RTO) |
|-------------------|------------------|-------------------------------|
| **CRM Application** | 99.5% | < 10 minutes |
| **REST API** | 99.5% | < 10 minutes |
| **File Upload/Download** | 99.0% | < 15 minutes |
| **MongoDB** | 99.95% | < 5 minutes |
| **Azure Blob Storage** | 99.9% | < 10 minutes |

**Exclusions:**
- Scheduled maintenance windows (announced 48 hours in advance)
- User-side network failures
- Third-party service outages (Azure infrastructure)

---

## 11. Implementation Plan & Timeline

### 11.1 R1: Core CRM System (Current Phase)

**Duration:** 8 weeks

**Milestones:**
- ✅ Week 1-2: Database schema design and API contracts finalized
- ✅ Week 2-3: Backend API development (CRUD operations)
- 🔄 Week 3-4: Frontend components (Summary Dashboard, All Requests)
- 🔄 Week 4-5: Request Form with validation and file upload
- 📅 Week 5-6: My Tasks view and Cancel functionality
- 📅 Week 6-7: Export service and audit logging
- 📅 Week 7-8: Integration testing, bug fixes, UAT

**Owner:** Full-stack team (2 backend, 2 frontend developers)

**Deliverables:**
- Fully functional CRM application with 5 modules
- REST API with 9 endpoints
- Database with requests and audit logs collections
- File upload to Azure Blob Storage
- Export functionality (CSV/Excel)
- Comprehensive audit trail

**Dependencies:**
- Azure Blob Storage (uflpa container) provisioned
- MongoDB multi-tenant setup complete
- JWT authentication system in place
- FusionCharts license procured

---

### 11.2 R2: Enhanced Features & Integrations (Planned)

**Duration:** 6 weeks (Planned Q1 2026)

**Potential Features:**
- Email notifications for assignments and status changes
- Advanced workflow automation (approval chains)
- Custom fields and request templates
- SLA tracking with automatic escalation
- Integration with external CRM systems
- Mobile-responsive design improvements
- Bulk operations (bulk assign, bulk update)
- Advanced reporting and analytics

**Owner:** TBD based on business priorities

**Deliverables:** TBD based on user feedback and requirements

---

### 11.3 R3: AI & Automation (Future)

**Duration:** 8 weeks (Planned Q3 2026)

**Potential Features:**
- AI-powered duplicate detection (fuzzy matching)
- Automated request categorization using NLP
- Predictive analytics for resolution time
- Chatbot for request status inquiries
- Smart assignment based on workload and expertise
- Automated compliance checks

**Owner:** TBD

**Deliverables:** TBD based on AI/ML capabilities and ROI analysis

---

### 11.4 Rollout Strategy

**Development Environment:**
- Feature branch: `feature/crm-r1`
- Code review by senior developers
- Unit tests: 80%+ coverage
- Integration tests for multi-tenant scenarios

**Staging Environment:**
- Deploy to staging for 2 weeks
- QA team manual testing
- Pilot with 3 friendly customers
- Performance testing with 200 concurrent users
- Security penetration testing

**Production Rollout:**
- Canary deployment: 20% of tenants for 1 week
- Monitor metrics for anomalies
- Gradual rollout: 50%, 100% over 2 weeks
- Rollback plan: Revert to previous version within 30 minutes if critical issues
- Post-deployment monitoring for 48 hours

---

## 12. Testing & Validation

### 12.1 Unit Testing Strategy

**Backend Tests:**
- Request Service: CRUD operations, duplicate detection, status transitions
- File Service: Upload, download, deletion, validation
- Export Service: CSV/Excel generation, filtered exports
- Audit Logger: Log creation, querying

**Frontend Tests:**
- React Components: Rendering, user interactions, form validation
- API Integration: Mock API responses, error handling
- State Management: Context updates, data flow

**Coverage Target:** 80% code coverage

**Tools:** Jest, React Testing Library, Mocha, Sinon

---

### 12.2 Integration Testing

**Scenarios:**
1. **End-to-End Request Creation:**
   - User fills request form
   - System validates and detects no duplicates
   - Request saved to database
   - Audit log entry created
   - Request appears in All Requests and assignee's My Tasks
   - KPIs updated on dashboard

2. **Multi-Tenant Isolation:**
   - Create requests for Tenant A and Tenant B
   - Verify Tenant A users only see Tenant A requests
   - Verify Tenant B users only see Tenant B requests
   - Verify no cross-tenant data leakage

3. **File Upload and Download:**
   - User uploads file to request
   - File saved to Azure Blob Storage
   - File metadata saved in request document
   - User downloads file successfully
   - Verify tenant isolation for file access

4. **Request Cancellation:**
   - User selects multiple requests
   - Clicks Cancel action
   - Enters cancellation reason
   - Requests marked as cancelled (soft delete)
   - Audit log captures cancellation details

5. **Export Functionality:**
   - User applies filters (status, type, customer)
   - Clicks Export button
   - CSV file generated with filtered data
   - All selected fields included
   - Only tenant-specific data exported

6. **Dashboard KPI Accuracy:**
   - Create, update, and close various requests
   - Verify KPI calculations are accurate
   - Verify charts reflect correct data
   - Verify My Tasks counts are correct

**Tools:** Postman for API testing, Cypress for E2E testing, Playwright for browser automation

---

### 12.3 Performance Testing

**Load Test Scenarios:**
1. **Concurrent Users:**
   - 500 concurrent users accessing CRM
   - Verify page load times < 2s
   - Verify no database connection pool exhaustion

2. **Request Creation Burst:**
   - 100 requests created within 10 seconds
   - Verify all requests saved correctly
   - Verify no duplicate detection failures

3. **Large Dataset Export:**
   - Export 5,000 requests
   - Verify export completes < 60 seconds
   - Verify no memory issues

4. **Dashboard Chart Rendering:**
   - 50 users accessing dashboard simultaneously
   - Verify chart rendering < 1 second
   - Verify no UI freezing

**Tools:** Apache JMeter, Artillery, k6

---

### 12.4 Security Testing

**Penetration Testing:**
- Attempt to access requests from different tenant
- Attempt to upload malicious files
- Attempt XSS injection in comments field
- Attempt SQL/NoSQL injection in search queries
- Attempt to download files from other tenants
- Attempt brute force login

**Compliance Audit:**
- Verify TLS encryption for all connections
- Verify no secrets in logs or error messages
- Verify audit logs capture all required actions
- Verify data retention policies implemented
- Verify file storage security (no public access)

**Tools:** OWASP ZAP, Burp Suite, manual code review

---

### 12.5 User Acceptance Testing (UAT)

**Test Users:**
- 5 internal stakeholders from different teams
- 3 pilot customers (external users)
- Test on staging environment with realistic data

**Test Scenarios:**
1. Create new request with all fields
2. Upload files to request
3. Update request status and comments
4. Assign request to another user
5. Cancel request with reason
6. Export filtered request list
7. View dashboard KPIs and charts
8. Access My Tasks view
9. Search and filter requests
10. Verify audit trail for all actions

**Acceptance Criteria:**
- All scenarios pass for all test users
- No critical bugs reported
- User feedback scores ≥ 8/10 on usability survey
- Performance meets targets (page load < 2s)

---

## 13. Recommendations & Trade-offs

### 13.1 Technology Choices

**Decision: Ant Design vs. Material-UI**

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| **Ant Design** | ✅ Enterprise-focused components<br>✅ Comprehensive table component<br>✅ Better TypeScript support<br>✅ Built-in form validation | ❌ Larger bundle size<br>❌ Less customizable | **✅ SELECTED** |
| **Material-UI** | ✅ More popular<br>✅ Extensive ecosystem | ❌ More boilerplate for complex forms<br>❌ Table component less feature-rich | ❌ Not selected |

**Rationale:** Ant Design is better suited for enterprise data management applications with complex tables and forms. The built-in table component with sorting, filtering, and pagination matches CRM requirements perfectly.

---

**Decision: FusionCharts vs. Chart.js**

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| **FusionCharts** | ✅ Rich visualization library<br>✅ Interactive charts<br>✅ Heat map support<br>✅ Export capabilities | ❌ Commercial license required<br>❌ Larger bundle size | **✅ SELECTED** |
| **Chart.js** | ✅ Free and open-source<br>✅ Smaller bundle size<br>✅ Active community | ❌ Limited chart types<br>❌ No heat map out-of-box<br>❌ Less interactive | ❌ Not selected |

**Rationale:** FusionCharts provides advanced visualization capabilities required for comprehensive dashboard. Heat map for regulation distribution and interactive drill-down features justify the license cost.

---

**Decision: MongoDB vs. PostgreSQL**

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| **MongoDB** | ✅ Flexible schema for evolving requirements<br>✅ Easy horizontal scaling<br>✅ JSON-like documents<br>✅ Already used in platform | ❌ No ACID transactions (older versions)<br>❌ Less mature query optimization | **✅ SELECTED** |
| **PostgreSQL** | ✅ ACID transactions<br>✅ Strong consistency<br>✅ Advanced query features | ❌ Schema changes require migrations<br>❌ More complex to scale horizontally | ❌ Not selected |

**Rationale:** MongoDB aligns with existing platform architecture. Flexible schema supports future custom fields without migrations. Multi-tenant data isolation is simpler with MongoDB's collection-per-tenant model.

---

### 13.2 Feature Prioritization

**Decision: Role-Agnostic Access (R1) vs. Role-Based Access Control (Future)**

**Selected: Role-Agnostic Access**
- All tenant users have equal permissions
- Simpler implementation and testing
- Faster time to market
- Addresses 90% of use cases

**Rationale:** Initial user research shows most tenants have small teams (5-20 users) where everyone needs full access. Adding RBAC adds complexity without immediate value. Can be added in R2 based on customer feedback.

---

**Decision: Duplicate Detection (R1) vs. AI-Powered Smart Matching (Future)**

**Selected: Simple Duplicate Detection**
- Exact match on customer + requestType + regulations
- User can override with confirmation
- Low false positive rate

**Future: AI-Powered Matching**
- Fuzzy string matching for customer names
- NLP for semantic similarity in comments
- Machine learning model for duplicate prediction

**Rationale:** Simple duplicate detection is sufficient for R1 and has clear implementation path. AI matching requires training data and ongoing model maintenance, better suited for R3 after collecting usage data.

---

### 13.3 Architecture Trade-offs

**Decision: Synchronous Export vs. Asynchronous Export**

**Selected: Synchronous Export (R1)**
- Simple implementation
- Immediate user feedback
- Works for datasets < 5,000 records

**Future: Asynchronous Export (R2)**
- Background job processing
- Email with download link when ready
- Supports very large datasets (100,000+ records)

**Rationale:** Synchronous export meets R1 requirements (most tenants have < 1,000 requests). Async export adds complexity (job queue, email service, status tracking) without immediate need.

---

**Decision: Real-Time Collaboration vs. Optimistic Locking**

**Selected: Optimistic Locking**
- Detect concurrent updates via lastModifiedAt
- Show error message if conflict detected
- User manually resolves conflict

**Future: Real-Time Collaboration**
- WebSocket for live updates
- Show who is viewing/editing request
- Collaborative editing like Google Docs

**Rationale:** Concurrent updates are rare in CRM workflow (requests typically updated by assigned user only). Real-time collaboration adds significant complexity without addressing common use case.

---

## 14. Open Questions & Decisions Needed

### 14.1 Product/Business Decisions

| Question | Options | Proposed Default | Stakeholder | Priority |
|----------|---------|------------------|-------------|----------|
| **Should we implement SLA tracking?** | (A) Yes, with automatic escalation<br>(B) Yes, but manual only<br>(C) No, deadline tracking is sufficient | (B) Yes, but manual (add in R2) | Product Manager | Medium |
| **What should be the default request status?** | (A) Open<br>(B) Pending Review<br>(C) User selects | (A) Open | Product Manager | High |
| **Should assignee be mandatory when creating request?** | (A) Yes, must assign immediately<br>(B) No, can assign later | (B) No, can assign later | Product Manager | Medium |
| **Should we allow bulk operations?** | (A) Yes, bulk assign and bulk update<br>(B) Only bulk cancel<br>(C) No bulk operations | (B) Only bulk cancel (R1) | Product Manager | Low |
| **Should customers have read-only portal access?** | (A) Yes, customers can view their requests<br>(B) No, internal only | (B) No, internal only (add in R3) | Product Manager | Low |

---

### 14.2 Technical Decisions

| Question | Options | Proposed Default | Stakeholder | Priority |
|----------|---------|------------------|-------------|----------|
| **Should we implement caching for dashboard KPIs?** | (A) Yes, Redis cache for 5 minutes<br>(B) No, always fetch from database | (A) Yes, Redis cache | Tech Lead | Medium |
| **What should be the maximum file size?** | (A) 10 MB<br>(B) 50 MB<br>(C) 100 MB | (B) 50 MB | Tech Lead | High |
| **Should we version control request updates?** | (A) Yes, store full history of changes<br>(B) No, only audit log | (B) No, only audit log | Tech Lead | Medium |
| **Should we implement request templates?** | (A) Yes, predefined templates for common types<br>(B) No, free-form entry only | (B) No (add in R2 if requested) | Tech Lead | Low |
| **Should we add request priority field?** | (A) Yes (High, Medium, Low)<br>(B) No, use deadline only | (B) No, use deadline only | Tech Lead | Medium |

---

### 14.3 Compliance & Legal

| Question | Options | Proposed Default | Stakeholder | Priority |
|----------|---------|------------------|-------------|----------|
| **What is the audit log retention period?** | (A) 3 years<br>(B) 7 years<br>(C) Forever | (B) 7 years (SOX requirement) | Legal | High |
| **Should we implement data export for GDPR compliance?** | (A) Yes, users can export all their data<br>(B) No, manual process | (A) Yes, add in R2 | Legal | High |
| **Should we scan uploaded files for malware?** | (A) Yes, integrate antivirus scanning<br>(B) No, rely on file type validation | (B) No (add in R2 if budget allows) | Security | Medium |
| **Do we need to anonymize user data after account deletion?** | (A) Yes, replace names with "Deleted User"<br>(B) No, keep full audit trail | (A) Yes, for GDPR compliance | Legal | High |

---

### 14.4 UX/Design

| Question | Options | Proposed Default | Stakeholder | Priority |
|----------|---------|------------------|-------------|----------|
| **Should dashboard auto-refresh?** | (A) Yes, every 60 seconds<br>(B) No, manual refresh only | (A) Yes, every 60 seconds | UX Designer | Medium |
| **Should we show request history timeline?** | (A) Yes, visual timeline of status changes<br>(B) No, just audit log | (B) No (add in R2) | UX Designer | Low |
| **Should we implement dark mode?** | (A) Yes<br>(B) No | (B) No (add in R3) | UX Designer | Low |
| **How should overdue requests be highlighted?** | (A) Red background<br>(B) Red badge<br>(C) Red text + icon | (C) Red text + icon | UX Designer | Medium |
| **Should we add keyboard shortcuts?** | (A) Yes (Ctrl+N for new request, etc.)<br>(B) No | (B) No (add in R2) | UX Designer | Low |

---

## 15. Appendices

### Appendix A: Request Status State Machine

```
     ┌─────┐
     │ Open│
     └──┬──┘
        │
        ├──────────┐
        │          │
        ↓          ↓
  ┌──────────┐  ┌──────────┐
  │In Progress│  │Cancelled │ (terminal)
  └─────┬────┘  └──────────┘
        │
        ├──────────┐
        │          │
        ↓          ↓
  ┌──────────┐  ┌──────────┐
  │ Resolved │  │Cancelled │ (terminal)
  └─────┬────┘  └──────────┘
        │
        ↓
   ┌──────┐
   │Closed│ (terminal)
   └──────┘
```

**Valid Transitions:**
- Open → In Progress, Cancelled
- In Progress → Resolved, Open, Cancelled
- Resolved → Closed, In Progress
- Closed → (no transitions)
- Cancelled → (no transitions)

---

### Appendix B: Database Query Examples

**Find all open requests for a tenant:**
```javascript
db.requests.find({
  tenantNumber: "TENANT001",
  status: "Open"
}).sort({ requestDate: -1 })
```

**Find overdue requests:**
```javascript
db.requests.find({
  tenantNumber: "TENANT001",
  status: { $in: ["Open", "In Progress"] },
  deadline: { $lt: new Date() }
})
```

**Calculate average resolution time:**
```javascript
db.requests.aggregate([
  {
    $match: {
      tenantNumber: "TENANT001",
      status: "Closed"
    }
  },
  {
    $project: {
      resolutionTime: {
        $divide: [
          { $subtract: ["$updatedAt", "$createdAt"] },
          1000 * 60 * 60 * 24  // Convert to days
        ]
      }
    }
  },
  {
    $group: {
      _id: null,
      avgResolutionTime: { $avg: "$resolutionTime" }
    }
  }
])
```

**Get request type breakdown:**
```javascript
db.requests.aggregate([
  {
    $match: { tenantNumber: "TENANT001" }
  },
  {
    $group: {
      _id: "$requestType",
      count: { $sum: 1 }
    }
  },
  {
    $sort: { count: -1 }
  }
])
```

---

### Appendix C: Monitoring Dashboard Queries

**Application Insights KQL Queries:**

**API Response Time:**
```kql
requests
| where name startswith "GET /api/crm"
| summarize 
    p50 = percentile(duration, 50),
    p95 = percentile(duration, 95),
    p99 = percentile(duration, 99)
  by bin(timestamp, 5m), name
| render timechart
```

**API Error Rate:**
```kql
requests
| where name startswith "GET /api/crm" or name startswith "POST /api/crm"
| summarize 
    Total = count(),
    Errors = countif(resultCode >= 400)
  by bin(timestamp, 5m)
| extend ErrorRate = (Errors * 100.0) / Total
| project timestamp, ErrorRate
| render timechart
```

**File Upload Success Rate:**
```kql
customEvents
| where name == "file_upload"
| extend Success = tobool(customDimensions["success"])
| summarize 
    Total = count(),
    Successful = countif(Success == true)
  by bin(timestamp, 1h)
| extend SuccessRate = (Successful * 100.0) / Total
```

**Database Query Performance:**
```kql
dependencies
| where target contains "mongodb"
| summarize 
    p50 = percentile(duration, 50),
    p95 = percentile(duration, 95),
    p99 = percentile(duration, 99)
  by bin(timestamp, 5m)
| render timechart
```

---

### Appendix D: Troubleshooting Runbook

**Issue: User Cannot Upload File**

**Diagnostic Steps:**
1. Check file size and type
   ```javascript
   // Allowed types
   const allowedTypes = ['application/pdf', 'application/vnd.ms-excel', 
                         'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                         'image/jpeg', 'image/png', 'text/csv']
   // Max size: 50 MB
   ```

2. Verify Azure Blob Storage connection
   ```bash
   # Test connection
   az storage blob list --container-name uflpa --account-name <storage_account>
   ```

3. Check application logs for errors
   ```kql
   traces
   | where message contains "file upload" and severityLevel > 2
   | order by timestamp desc
   | take 20
   ```

4. Verify user has valid JWT token

**Common Resolutions:**
- File exceeds 50 MB limit → Ask user to compress or split file
- File type not allowed → Convert to supported format
- Azure storage quota exceeded → Increase storage quota
- Network timeout → Retry upload

---

**Issue: Duplicate Request Not Detected**

**Diagnostic Steps:**
1. Check duplicate detection logic
   ```javascript
   const existing = await Request.findOne({
     tenantNumber: user.tenantNumber,
     customer: requestData.customer,
     requestType: requestData.requestType,
     regulations: { $all: requestData.regulations }
   })
   ```

2. Verify case sensitivity in comparison
3. Check if regulations array order matters
4. Review audit logs for similar requests

**Common Resolutions:**
- Customer name has different capitalization → Normalize to lowercase
- Regulations in different order → Sort array before comparison
- Duplicate detection too strict → Relax matching criteria

---

**Issue: Dashboard KPIs Incorrect**

**Diagnostic Steps:**
1. Verify tenant filtering in queries
2. Check date range for trend calculations
3. Verify status values match expected enum
4. Check for cached data (if caching implemented)

**Common Resolutions:**
- Clear cache and recalculate
- Verify database indexes are used
- Check for data inconsistencies (orphaned records)
- Review aggregation pipeline logic

---

**End of Design Document**
