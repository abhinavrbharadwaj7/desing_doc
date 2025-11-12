# FMD Notification System — Real-time Compliance Status Updates

**A scalable, multi-tenant notification system for the Acquis Compliance Platform**

---

## 1. Summary

The FMD (Full Material Disclosure) Notification System is a real-time notification solution that alerts users when compliance status changes occur in the Acquis Compliance Platform. The system delivers instant in-app notifications using Server-Sent Events (SSE) with Redis pub/sub for horizontal scaling across CDN-distributed backend instances. The initial implementation focuses on in-app notifications for supplier data approval workflows, with email notifications planned for future phases.

**Key Outcomes:**
- Real-time compliance status change notifications
- Multi-tenant isolation with tenant-specific databases
- Horizontal scalability across Azure CDN instances
- Intelligent notification grouping to prevent spam
- Persistent notification history with read/unread tracking

**Recommended Next Steps:**
1. Deploy the notification system to production
2. Monitor performance metrics and user engagement
3. Plan Phase 2: Email notification integration
4. Consider expanding notification triggers to additional compliance workflows

---

## 2. Overview

### 2.1 Purpose

The FMD Notification System addresses the critical need for users to stay informed about compliance status changes in real-time without manually refreshing or checking multiple parts of the application. When a user approves supplier data that affects FMD component compliance, all relevant users in the tenant receive immediate notification.

### 2.2 Scope

**In Scope:**
- Real-time in-app notifications via SSE
- Notification grouping for similar events (5-minute window)
- Multi-tenant data isolation
- Notification history with pagination
- Read/unread status tracking
- Mark as read functionality (individual and bulk)
- Unread count badge
- Integration with existing Campaign Manager and Responsible Minerals modules

**Out of Scope (Future Phases):**
- Email notifications
- Push notifications for mobile devices
- Notification preferences/settings
- Notification filtering by module or regulation
- Webhook integrations for third-party systems

### 2.3 Goals & Success Metrics

**Goals:**
1. Reduce time-to-awareness of compliance status changes from hours/days to seconds
2. Prevent notification fatigue through intelligent grouping
3. Ensure 99.9% notification delivery reliability
4. Support horizontal scaling for production CDN environment
5. Maintain sub-500ms notification delivery latency

**Success Metrics:**
- Notification delivery rate: ≥ 99.9%
- Average delivery latency: < 500ms
- SSE connection uptime: ≥ 99.5%
- User engagement rate: ≥ 70% of notifications clicked within 24 hours
- Zero cross-tenant data leakage incidents

---

## 3. Key Definitions

| Term | Definition |
|------|------------|
| **FMD** | Full Material Disclosure - compliance data about product materials |
| **SSE** | Server-Sent Events - HTTP standard for server-to-client streaming |
| **Redis Pub/Sub** | Redis publish/subscribe messaging pattern for inter-process communication |
| **Tenant** | Individual customer organization in the multi-tenant SaaS platform |
| **Notification Grouping** | Consolidating multiple similar notifications into a single message |
| **CDN** | Content Delivery Network - Azure CDN used for load distribution |
| **Campaign Manager** | Module for managing supplier data collection campaigns |
| **Responsible Minerals** | Module for CMRT/EMRT compliance tracking |
| **REACH** | EU regulation on chemical substances |
| **CMRT** | Conflict Minerals Reporting Template |
| **EMRT** | Extended Minerals Reporting Template |

---

## 4. Proposed Design (High-Level)

### 4.1 User Flow: Receiving a Notification

```
User logs into Acquis Platform
    ↓
SSE connection established automatically
    ↓
User performs action (e.g., approves supplier data)
    ↓
Backend detects compliance status change
    ↓
Notification created and published to Redis
    ↓
Redis broadcasts to relevant backend instance
    ↓
SSE sends notification to all connected tenant users
    ↓
Notification appears in bell icon with unread count
    ↓
User clicks notification bell to view details
    ↓
User marks notification as read
```

### 4.2 Component Responsibilities

| Component | Responsibility |
|-----------|---------------|
| **SSE Manager** | Manages active connections, handles Redis pub/sub, routes notifications to correct users |
| **Notifications Plugin** | Creates notifications, applies grouping logic, manages timeouts, persists to database |
| **Notifications Routes** | Provides REST API endpoints, establishes SSE connections, handles mark-as-read operations |
| **Redux Store** | Manages front-end notification state, handles optimistic updates |
| **Notification Bell Component** | Displays unread count badge, shows notification drawer, triggers mark-as-read actions |

### 4.3 Data Flow

```
[User Action] → [API Endpoint]
                      ↓
              [Business Logic Validates Change]
                      ↓
              [createNotification() called]
                      ↓
              [Check for existing grouped notification]
                      ↓
         ┌────────────┴────────────┐
         ↓                         ↓
   [New Group]             [Existing Group]
         ↓                         ↓
   [Create Record]          [Update Count]
         ↓                         ↓
   [Set 5-min timeout]      [Reset timeout]
         ↓                         ↓
         └────────────┬────────────┘
                      ↓
              [Save to MongoDB]
                      ↓
              [Publish to Redis]
                      ↓
         [Redis broadcasts to all instances]
                      ↓
         [SSE Manager sends to active connections]
                      ↓
              [Front-end receives notification]
                      ↓
              [Redux state updated]
                      ↓
              [UI re-renders with new notification]
```

---

## 5. System Architecture

### 5.1 Logical Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                      Azure CDN Layer                          │
│  (Load balances requests across backend instances)            │
└─────────────────┬────────────────────────┬───────────────────┘
                  │                        │
        ┌─────────▼─────────┐    ┌────────▼──────────┐
        │  Backend Instance 1│    │ Backend Instance 2 │
        │  (Fastify Server)  │    │  (Fastify Server)  │
        │                    │    │                    │
        │  ┌──────────────┐ │    │  ┌──────────────┐  │
        │  │ SSE Manager  │ │    │  │ SSE Manager  │  │
        │  └──────────────┘ │    │  └──────────────┘  │
        │  ┌──────────────┐ │    │  ┌──────────────┐  │
        │  │ Notifications│ │    │  │ Notifications│  │
        │  │   Plugin     │ │    │  │   Plugin     │  │
        │  └──────────────┘ │    │  └──────────────┘  │
        └─────────┬─────────┘    └────────┬───────────┘
                  │                       │
                  │  ┌────────────────┐   │
                  └──► Azure Redis    ◄───┘
                     │ Cache (Pub/Sub)│
                     └────────────────┘
                            │
                     ┌──────▼──────┐
                     │   MongoDB   │
                     │ (Multi-tenant│
                     │  Databases)  │
                     └─────────────┘

┌──────────────────────────────────────────────────────────────┐
│                    Front-End (React)                          │
│  ┌────────────┐  ┌────────────┐  ┌────────────────┐         │
│  │ SSE Client │  │Redux Store │  │ Notification   │         │
│  │ Connection │◄─┤            ├─►│ Bell Component │         │
│  └────────────┘  └────────────┘  └────────────────┘         │
└──────────────────────────────────────────────────────────────┘
```

### 5.2 Backend Services

**Fastify Server:**
- REST API endpoints for notification operations
- SSE endpoint for real-time connections
- Multi-tenant database routing
- JWT authentication and authorization

**SSE Manager:**
- Active connection map (in-memory)
- Redis subscriber for cross-instance communication
- Connection lifecycle management (add, remove, cleanup)
- Tenant isolation enforcement

**Notifications Plugin:**
- Notification creation decorator
- Grouping logic with timeout management
- Database persistence
- Redis publish operations

### 5.3 Frontend Considerations

**React Components:**
- Notification Bell: Displays unread count, opens drawer
- Notification Drawer: Lists all notifications with tabs (All/Unread)
- Notification Item: Individual notification display with mark-as-read action

**State Management:**
- Redux Toolkit for centralized state
- Optimistic updates for mark-as-read operations
- SSE connection state tracking
- Automatic reconnection on connection loss

**Performance Optimizations:**
- Pagination for notification history (10 per page)
- Virtual scrolling for large notification lists
- Debounced mark-as-read API calls
- Memoized selectors for derived state

### 5.4 Third-Party Integrations

| Service | Purpose | Configuration |
|---------|---------|---------------|
| **Azure Redis Cache** | Pub/sub messaging, connection metadata | Host: acquiscomplifmqaapiredis.redis.cache.windows.net, Port: 6380, TLS enabled |
| **Azure CDN** | Load distribution, SSL termination | Configured for SSE long-lived connections |
| **MongoDB** | Persistent storage | Multi-tenant databases, replica set for HA |

---

## 6. Database Design

### 6.1 Notifications Collection Schema

```javascript
{
  _id: ObjectId,                    // Unique notification identifier
  userIds: [String],                // Array of user email addresses
  message: String,                  // Short notification message
  description: String,              // Detailed notification content
  type: String,                     // "info" | "success" | "warning" | "error"
  groupId: String,                  // Grouping identifier (e.g., "newSupplierResponse")
  triggerSource: String,            // Source module (e.g., "Campaign Manager")
  applicableModules: [String],      // Relevant modules
  metadata: {                       // Flexible metadata object
    count: Number,                  // Number of grouped items
    supplierIds: [String],          // Related supplier IDs
    campaignIds: [String],          // Related campaign IDs
    regulationType: String,         // REACH, CMRT, EMRT, etc.
    productName: String,            // Affected product
    oldStatus: String,              // Previous compliance status
    newStatus: String,              // New compliance status
    changedBy: String,              // User who triggered change
    changeDate: Date                // When change occurred
  },
  readBy: [String],                 // Users who marked as read
  isReady: Boolean,                 // Grouping timeout completed
  timestamp: Date,                  // Creation timestamp
  createdAt: Date,                  // MongoDB timestamp
  updatedAt: Date                   // MongoDB timestamp
}
```

### 6.2 Indexes

```javascript
// Performance indexes
db.notifications.createIndex({ userIds: 1, timestamp: -1 })
db.notifications.createIndex({ userIds: 1, readBy: 1, isReady: 1 })
db.notifications.createIndex({ groupId: 1, isReady: 1 })
db.notifications.createIndex({ timestamp: -1 })

// TTL index for automatic cleanup (optional - 90 days retention)
db.notifications.createIndex({ timestamp: 1 }, { expireAfterSeconds: 7776000 })
```

### 6.3 Data Retention Rules

- **Active Notifications:** Retained indefinitely while unread
- **Read Notifications:** Retained for 90 days, then auto-deleted via TTL index
- **Grouped Notifications:** Retained as single record with aggregated count
- **Backup Policy:** Included in daily MongoDB backups

---

## 7. API Contracts

### 7.1 Establish SSE Connection

**Endpoint:** `GET /notifications`

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response:** Stream (text/event-stream)
```
Content-Type: text/event-stream
Cache-Control: no-cache, no-store, must-revalidate
Connection: keep-alive

data: {"message": "SSE connection established", "timestamp": 1643723400000}

data: {"_id": "67890", "message": "(1) new pending responses to approve", "type": "info", "timestamp": "2025-11-12T10:00:00Z"}
```

**Error Responses:**
- `400 Bad Request` - Missing authorization header
- `401 Unauthorized` - Invalid or expired token
- `500 Internal Server Error` - Server error

---

### 7.2 Get Notification History

**Endpoint:** `GET /notifications/history`

**Query Parameters:**
```
page: number (default: 1)
limit: number (default: 20, max: 100)
status: "unread" | undefined (filter by unread only)
```

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response:** `200 OK`
```json
{
  "message": "Notifications fetched successfully",
  "data": {
    "notifications": [
      {
        "_id": "67890",
        "message": "(3) new pending responses to approve",
        "description": "You have 3 new supplier responses to approve in the Campaign Manager module under the Pending Approvals Tab.",
        "type": "info",
        "groupId": "newSupplierResponse",
        "triggerSource": "Campaign Manager",
        "applicableModules": ["Campaign Manager"],
        "metadata": {
          "count": 3,
          "supplierIds": ["sup123", "sup456", "sup789"],
          "campaignIds": ["camp001"]
        },
        "readBy": [],
        "isReady": true,
        "timestamp": "2025-11-12T10:00:00Z"
      }
    ],
    "total": 50,
    "unreadCount": 15,
    "currentPage": 1,
    "totalPages": 5
  }
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid token
- `500 Internal Server Error` - Database error

---

### 7.3 Get Unread Count

**Endpoint:** `GET /notifications/unread-count`

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response:** `200 OK`
```json
{
  "message": "Unread notifications count fetched successfully",
  "unreadCount": 15
}
```

---

### 7.4 Mark Notifications as Read

**Endpoint:** `POST /notifications/mark-as-read`

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "notificationIds": ["67890", "67891", "67892"]
}
```

**Response:** `200 OK`
```json
{
  "message": "Notifications marked as read successfully",
  "updatedCount": 3
}
```

**Error Responses:**
- `400 Bad Request` - Missing or invalid notificationIds
- `401 Unauthorized` - Invalid token
- `500 Internal Server Error` - Database error

---

### 7.5 Mark All Notifications as Read

**Endpoint:** `POST /notifications/mark-all-as-read`

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body:** `{}` (empty)

**Response:** `200 OK`
```json
{
  "message": "All notifications marked as read successfully",
  "updatedCount": 15
}
```

---

### 7.6 Authentication Model

**JWT Token Structure:**
```javascript
{
  emailAddress: "user@company.com",
  tenantNumber: "TENANT001",
  userId: "user123",
  role: "admin",
  iat: 1643723400,
  exp: 1643809800
}
```

**Token Validation:**
- Verified using shared secret or public key
- Checked for expiration on every request
- User email and tenant number extracted for authorization

**Tenant Isolation:**
- All database queries filtered by tenant number
- SSE connections tagged with tenant number
- Redis pub/sub includes tenant number for routing

---

## 8. Failure Scenarios & Mitigations

### 8.1 SSE Connection Failures

**Scenario:** User's SSE connection drops due to network issues or server restart

**Impact:** User stops receiving real-time notifications

**Mitigation:**
- **Auto-reconnection:** Front-end automatically reconnects with exponential backoff (1s, 2s, 4s, 8s, max 30s)
- **Missed notification recovery:** On reconnection, fetch notification history to catch any missed notifications
- **User feedback:** Show "Connecting..." status in notification bell during reconnection

**Detection:** Front-end monitors EventSource `error` and `close` events

---

### 8.2 Redis Connection Failure

**Scenario:** Redis cache becomes unavailable

**Impact:** Cross-instance notification delivery fails; only same-instance notifications work

**Mitigation:**
- **Graceful degradation:** SSE connections continue working for same-instance notifications
- **Health check:** Monitor Redis connection status and alert operations team
- **Connection retry:** Automatic reconnection with exponential backoff
- **Circuit breaker:** Prevent cascading failures by temporarily disabling Redis operations

**Detection:** Redis client emits `error` event; health check endpoint reports degraded status

---

### 8.3 MongoDB Connection Failure

**Scenario:** Tenant database becomes unavailable

**Impact:** Cannot persist new notifications or fetch history

**Mitigation:**
- **Retry logic:** 3 retry attempts with exponential backoff (1s, 2s, 4s)
- **Error response:** Return 503 Service Unavailable to client
- **Monitoring:** Alert on database connection failures
- **Fallback:** Consider in-memory queue for temporary notification storage (future enhancement)

**Detection:** MongoDB client throws connection errors; monitored via application logs

---

### 8.4 Notification Grouping Timeout Memory Leak

**Scenario:** Notification timeouts accumulate without cleanup

**Impact:** Memory usage grows unbounded, eventual server crash

**Mitigation:**
- **Timeout cleanup:** Always clear timeout when notification becomes ready
- **Periodic audit:** Log timeout map size every minute; alert if > 100 active timeouts
- **Timeout limits:** Set maximum grouping window (5 minutes) to bound memory growth
- **Server restart:** Deploy rolling restarts in production to clear accumulated state

**Detection:** Memory usage monitoring; application logs track timeout map size

---

### 8.5 CDN Routing Inconsistency

**Scenario:** CDN routes SSE connection to different instance than notification trigger

**Impact:** Notification not delivered to user (primary failure mode that required Redis)

**Mitigation:**
- **Redis pub/sub:** Ensures all instances receive notification events
- **Connection metadata:** Store user connection mapping in Redis for cross-instance visibility
- **Heartbeat:** Periodic keep-alive messages on SSE connections
- **Stale connection cleanup:** Remove connections from Redis after 5 minutes of inactivity

**Detection:** User reports missing notifications; monitor notification delivery rate

---

### 8.6 Cross-Tenant Data Leakage

**Scenario:** Bug in tenant filtering sends notification to wrong tenant

**Impact:** Data breach, compliance violation

**Mitigation:**
- **Multi-layer filtering:** Enforce tenant isolation at database, Redis, and SSE layers
- **Integration tests:** Comprehensive tests for tenant isolation
- **Code review:** Mandatory review of all tenant-filtering code
- **Audit logging:** Log all notification deliveries with tenant info for forensics

**Detection:** Automated tests; user reports; audit log analysis

---

### 8.7 Notification Spam (Grouping Failure)

**Scenario:** Grouping logic fails, users receive 50+ individual notifications

**Impact:** Notification fatigue, user disables notifications

**Mitigation:**
- **Rate limiting:** Maximum 10 notifications per user per minute
- **Grouping verification:** Unit tests for all grouping scenarios
- **Monitoring:** Track notifications per user per hour; alert on spikes
- **Emergency disable:** Admin API to temporarily disable notifications for a tenant

**Detection:** User complaints; monitoring dashboards show spike in notification count

---

## 9. Security & Privacy

### 9.1 Threat Model Highlights

| Threat | Impact | Mitigation |
|--------|--------|------------|
| **JWT Token Theft** | Attacker receives notifications for victim user | Short token expiry (8 hours), HTTPS only, secure storage |
| **Cross-Tenant Data Leakage** | User sees another tenant's notifications | Multi-layer tenant filtering, comprehensive testing |
| **XSS in Notification Content** | Malicious script execution in user's browser | Sanitize all notification content, CSP headers |
| **SSE Connection Hijacking** | Attacker intercepts notification stream | TLS encryption, token validation on connection |
| **Redis Command Injection** | Attacker executes arbitrary Redis commands | Use parameterized queries, disable dangerous commands |
| **MongoDB Injection** | Attacker accesses unauthorized data | Use ODM (Mongoose), validate all inputs |
| **Denial of Service** | Attacker floods system with notifications | Rate limiting, message queue backpressure |

---

### 9.2 Authentication & Authorization

**Authentication:**
- JWT token required for all endpoints
- Token includes user email, tenant number, and role
- Token validated on every request using shared secret
- SSE connection established only after successful token validation

**Authorization:**
- Users can only see notifications where `userIds` includes their email
- Tenant number from token must match notification's tenant database
- Mark-as-read operations validate user is in notification's `userIds` array
- No admin override capability to prevent privilege escalation

---

### 9.3 Data Encryption

**In Transit:**
- All API traffic over HTTPS (TLS 1.2+)
- SSE connections over HTTPS
- Redis connections use TLS (port 6380)
- MongoDB connections use TLS

**At Rest:**
- MongoDB data encrypted at rest via Azure encryption
- Redis data considered ephemeral (pub/sub messages not persisted)
- Notification content may include PII (user names) - treated as sensitive data

---

### 9.4 Secrets Management

**Environment Variables:**
- `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD` stored in Azure Key Vault
- MongoDB connection strings stored in Key Vault
- JWT signing secret rotated quarterly
- No secrets in code or Git repository

**Access Control:**
- Key Vault access restricted to production service principal
- Developers use separate development Redis/MongoDB instances
- Production secrets never shared via Slack/email

---

### 9.5 Compliance Considerations

**GDPR:**
- Notification content includes user names (PII)
- Users can request notification history deletion (right to erasure)
- 90-day retention aligns with legitimate interest
- Audit logs track who accessed notification data

**SOC 2:**
- TLS for all data in transit
- Access logging for all notification operations
- Regular security audits of notification code
- Incident response plan for data leakage

---

## 10. Non-Functional Requirements

### 10.1 Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Notification Delivery Latency** | < 500ms (p95) | Time from `createNotification()` to front-end receipt |
| **SSE Connection Establishment** | < 2 seconds | Time from login to SSE connected |
| **Notification History Load Time** | < 1 second | Time to fetch and render first page (10 notifications) |
| **Database Query Performance** | < 100ms (p95) | MongoDB query execution time |
| **Redis Pub/Sub Latency** | < 50ms (p95) | Time from publish to subscriber receipt |
| **Mark-as-Read API Response** | < 200ms (p95) | Time to update database and return response |

---

### 10.2 Scalability Plan

**Current Scale (Phase 1):**
- 500 concurrent users per tenant
- 10,000 notifications per day across all tenants
- 2 backend instances behind Azure CDN
- Single Redis instance (standard tier)
- MongoDB replica set (3 nodes)

**Future Scale (Phase 2 - 12 months):**
- 5,000 concurrent users per tenant
- 100,000 notifications per day
- 5+ backend instances with auto-scaling
- Redis cluster mode for high availability
- MongoDB sharding if single tenant grows large

**Scaling Strategies:**
- **Horizontal Backend Scaling:** Add more Fastify instances behind CDN
- **Redis Cluster:** Shard pub/sub channels by tenant for higher throughput
- **Database Sharding:** Separate high-volume tenants to dedicated MongoDB instances
- **CDN Optimization:** Use Azure CDN's geolocation routing for lower latency

---

### 10.3 Monitoring & Alerting Plan

**Key Metrics to Monitor:**

1. **SSE Connection Health:**
   - Active connection count per instance
   - Connection success/failure rate
   - Average connection duration
   - Reconnection frequency

2. **Notification Delivery:**
   - Notifications created per minute
   - Notification delivery success rate
   - End-to-end delivery latency (p50, p95, p99)
   - Notifications grouped vs. individual ratio

3. **Infrastructure:**
   - Redis connection pool utilization
   - Redis pub/sub latency
   - MongoDB query performance
   - Backend CPU/memory usage
   - Network throughput

4. **Business Metrics:**
   - Unread notification count per user
   - Notification click-through rate
   - Time-to-read (minutes from delivery to read)
   - User engagement with notifications

**Alerting Rules:**
- SSE connection failure rate > 5% for 5 minutes
- Notification delivery latency p95 > 2 seconds for 5 minutes
- Redis connection failure
- MongoDB connection failure
- Unread notification count > 100 for any user
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
| **SSE Connections** | 99.5% | < 5 minutes |
| **REST API Endpoints** | 99.9% | < 5 minutes |
| **Notification Delivery** | 99.9% | N/A (async) |
| **Redis Pub/Sub** | 99.9% | < 2 minutes |
| **MongoDB** | 99.95% | < 5 minutes |

**Exclusions:**
- Scheduled maintenance windows (announced 7 days in advance)
- User-side network failures
- Third-party service outages (Azure infrastructure)

---

## 11. Implementation Plan & Timeline

### 11.1 Phase 1: Core Notification System (Completed)

**Duration:** 6 weeks (Completed)

**Milestones:**
- ✅ Week 1-2: SSE Manager and basic connection handling
- ✅ Week 2-3: Notifications Plugin with database persistence
- ✅ Week 3-4: Redis integration for cross-instance communication
- ✅ Week 4-5: Front-end Redux integration and Notification Bell component
- ✅ Week 5-6: Notification grouping logic and timeout management
- ✅ Week 6: Production deployment and monitoring setup

**Owner:** Backend Team (3 developers), Frontend Team (2 developers)

**Deliverables:**
- SSE-based real-time notifications
- Notification history with pagination
- Mark-as-read functionality
- Notification grouping for supplier responses
- Production monitoring dashboards

**Dependencies:**
- Azure Redis Cache provisioned
- Multi-tenant MongoDB schema finalized
- JWT authentication system in place

---

### 11.2 Phase 2: Email Notifications (Planned)

**Duration:** 4 weeks (Planned Q1 2026)

**Milestones:**
- Week 1: Email service integration (SendGrid or Azure Communication Services)
- Week 2: Email template design and rendering engine
- Week 3: User preferences for email frequency (immediate, daily digest, off)
- Week 4: Testing, deployment, and user documentation

**Owner:** Backend Team (2 developers), Product Design (1 designer)

**Deliverables:**
- Email notification for compliance status changes
- User preferences UI for notification settings
- Email templates for different notification types
- Unsubscribe mechanism

**Dependencies:**
- Email service procurement and setup
- User preferences data model design
- GDPR compliance review for email communications

---

### 11.3 Phase 3: Enhanced Features (Future)

**Duration:** 6 weeks (Planned Q2 2026)

**Potential Features:**
- Push notifications for mobile app (if mobile app exists)
- Notification filtering by module, regulation, or product
- Notification snooze functionality
- Custom notification rules per user
- Webhook integrations for third-party systems
- Notification analytics dashboard for admins

**Owner:** TBD

**Deliverables:** TBD based on user feedback and business priorities

---

### 11.4 Rollout Strategy

**Development Environment:**
- Feature branch: `feature/fmd-notifications`
- Code review by 2+ senior developers
- Unit tests: 90%+ coverage
- Integration tests for multi-tenant scenarios

**Staging Environment:**
- Deploy to staging for 1 week
- QA team manual testing
- Load testing with 1,000 concurrent users
- Security penetration testing

**Production Rollout:**
- Canary deployment: 10% of tenants for 3 days
- Monitor metrics for anomalies
- Gradual rollout: 25%, 50%, 100% over 1 week
- Rollback plan: Revert to previous version within 15 minutes if critical issues

---

## 12. Testing & Validation

### 12.1 Unit Testing Strategy

**Backend Tests:**
- SSE Manager: Connection add/remove, Redis pub/sub message handling
- Notifications Plugin: Grouping logic, timeout management, database persistence
- Notifications Routes: API endpoint responses, authentication/authorization

**Frontend Tests:**
- Redux Actions: SSE connection, mark-as-read operations, state updates
- Redux Reducers: State transformations, notification count calculations
- Components: Notification Bell rendering, drawer interactions

**Coverage Target:** 90% code coverage

**Tools:** Jest, Mocha, Sinon for mocking

---

### 12.2 Integration Testing

**Scenarios:**
1. **End-to-End Notification Flow:**
   - Trigger compliance status change in Campaign Manager
   - Verify notification created in database
   - Verify notification delivered to all tenant users via SSE
   - Verify notification appears in front-end UI
   - Mark notification as read
   - Verify unread count decreases

2. **Multi-Tenant Isolation:**
   - Create notifications for Tenant A and Tenant B simultaneously
   - Verify Tenant A users only see Tenant A notifications
   - Verify Tenant B users only see Tenant B notifications

3. **Cross-Instance Delivery:**
   - Establish SSE connection on Instance 1
   - Trigger notification from Instance 2
   - Verify notification delivered via Redis pub/sub
   - Verify user receives notification on Instance 1

4. **Notification Grouping:**
   - Trigger 5 supplier responses within 2 minutes
   - Verify only 1 grouped notification created
   - Verify notification count increments to 5
   - Wait for 5-minute timeout
   - Verify grouped notification delivered to users

5. **SSE Reconnection:**
   - Establish SSE connection
   - Simulate network interruption (disconnect)
   - Verify front-end reconnects automatically
   - Verify missed notifications fetched on reconnection

**Tools:** Postman for API testing, Cypress for E2E testing

---

### 12.3 Performance Testing

**Load Test Scenarios:**
1. **Concurrent Connections:**
   - 1,000 concurrent SSE connections
   - Verify connection establishment < 2s
   - Verify memory usage < 2GB per instance

2. **Notification Burst:**
   - 1,000 notifications created within 10 seconds
   - Verify all notifications delivered < 5 seconds
   - Verify no dropped notifications

3. **Database Query Performance:**
   - 100 concurrent users fetching notification history
   - Verify query time < 100ms (p95)
   - Verify no connection pool exhaustion

4. **Redis Throughput:**
   - 10,000 pub/sub messages per second
   - Verify message delivery latency < 50ms (p95)
   - Verify no message loss

**Tools:** Apache JMeter, Artillery, k6

---

### 12.4 Security Testing

**Penetration Testing:**
- Attempt to access notifications from different tenant
- Attempt to hijack SSE connection with stolen token
- Attempt XSS injection in notification content
- Attempt SQL/NoSQL injection in API endpoints

**Compliance Audit:**
- Verify TLS encryption for all connections
- Verify no secrets in logs or error messages
- Verify audit logs for all notification operations
- Verify GDPR right-to-erasure implementation

**Tools:** OWASP ZAP, Burp Suite, manual code review

---

### 12.5 User Acceptance Testing (UAT)

**Test Users:**
- 5 internal stakeholders from different roles (admin, manager, analyst)
- Test on staging environment with realistic data

**Test Scenarios:**
1. Approve supplier data and verify notification received
2. View notification history and verify correct sorting
3. Mark individual notifications as read
4. Mark all notifications as read
5. Verify unread count badge accuracy
6. Test notification grouping with multiple responses
7. Test notification delivery on different browsers (Chrome, Edge, Safari)

**Acceptance Criteria:**
- All scenarios pass for all test users
- No critical bugs reported
- User feedback scores ≥ 8/10 on usability survey

---

## 13. Recommendations & Trade-offs

### 13.1 Technology Choices

**Decision: Server-Sent Events (SSE) vs. WebSockets**

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| **SSE** | ✅ Simpler protocol<br>✅ Auto-reconnection built-in<br>✅ Works over HTTP<br>✅ Better CDN compatibility | ❌ Unidirectional (server → client only)<br>❌ Limited browser support (IE) | **✅ SELECTED** |
| **WebSockets** | ✅ Bidirectional<br>✅ Lower latency | ❌ More complex to implement<br>❌ CDN compatibility issues<br>❌ Requires separate port/protocol | ❌ Not selected |

**Rationale:** SSE is sufficient for one-way notification delivery, simpler to implement, and works well with Azure CDN. WebSockets would be overkill for this use case.

---

**Decision: Redis Pub/Sub vs. Message Queue (RabbitMQ/Azure Service Bus)**

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| **Redis Pub/Sub** | ✅ Low latency (< 10ms)<br>✅ Simple setup<br>✅ Already using Redis | ❌ No message persistence<br>❌ No delivery guarantees | **✅ SELECTED** |
| **Message Queue** | ✅ Guaranteed delivery<br>✅ Message persistence<br>✅ Dead letter queue | ❌ Higher latency (50-100ms)<br>❌ More complex setup<br>❌ Additional service cost | ❌ Not selected |

**Rationale:** Notification delivery is best-effort (not critical transactions). Low latency is more important than guaranteed delivery. If notification fails, user can refresh or check history.

---

**Decision: In-App Notifications Only (Phase 1) vs. In-App + Email (Phase 1)**

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| **In-App Only** | ✅ Faster development<br>✅ No email service cost<br>✅ No spam concerns | ❌ User misses notifications when not logged in | **✅ SELECTED (Phase 1)** |
| **In-App + Email** | ✅ Better user reach<br>✅ Notification history via email | ❌ Longer development time<br>❌ Email deliverability issues<br>❌ User preferences complexity | ✅ PLANNED (Phase 2) |

**Rationale:** Ship faster with in-app only, gather user feedback, then add email in Phase 2 based on actual user needs.

---

### 13.2 Grouping Logic Trade-offs

**Decision: 5-Minute Grouping Window**

**Alternatives Considered:**
- **1 minute:** Too short, may still spam users with many individual notifications
- **10 minutes:** Too long, users wait too long for grouped notification
- **Dynamic (based on rate):** Too complex to implement and debug

**Selected: 5 minutes**
- Balances immediacy with spam reduction
- Long enough to group typical supplier response batches
- Short enough that users get timely notifications

**Future Optimization:** Consider adaptive timeout based on historical patterns (e.g., shorter timeout during business hours, longer timeout overnight).

---

### 13.3 Database Schema Trade-offs

**Decision: Embedded `metadata` Object vs. Separate Collections**

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| **Embedded `metadata`** | ✅ Single query to fetch all data<br>✅ Flexible schema<br>✅ Easier to add new fields | ❌ May grow unbounded<br>❌ Less structured | **✅ SELECTED** |
| **Separate Collections** | ✅ Normalized data<br>✅ Easier to query specific fields | ❌ Multiple queries (joins)<br>❌ More complex code | ❌ Not selected |

**Rationale:** Notifications are read-heavy, write-once documents. Embedding metadata simplifies queries and provides flexibility for different notification types without schema changes.

---

### 13.4 Front-End State Management

**Decision: Redux Toolkit vs. React Context**

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| **Redux Toolkit** | ✅ Centralized state<br>✅ DevTools for debugging<br>✅ Time-travel debugging<br>✅ Already used in project | ❌ More boilerplate<br>❌ Learning curve | **✅ SELECTED** |
| **React Context** | ✅ Simpler setup<br>✅ Built into React | ❌ No DevTools<br>❌ Performance issues with frequent updates | ❌ Not selected |

**Rationale:** Project already uses Redux Toolkit for other features. Consistency is more valuable than simplicity for a single feature.

---

## 14. Open Questions & Decisions Needed

### 14.1 Product/Business Decisions

| Question | Options | Proposed Default | Stakeholder | Priority |
|----------|---------|------------------|-------------|----------|
| **Should users be able to customize notification preferences?** | (A) No preferences - all users get all notifications<br>(B) Module-level toggles (Campaign Manager, Responsible Minerals, etc.)<br>(C) Fine-grained rules (by regulation, product, status change type) | (B) Module-level toggles | Product Manager | Medium |
| **How long should notification history be retained?** | (A) 30 days<br>(B) 90 days<br>(C) 1 year<br>(D) Forever | (B) 90 days | Product Manager + Legal | High |
| **Should we send email notifications for critical compliance changes?** | (A) Yes, always<br>(B) Yes, user opt-in<br>(C) No, in-app only | (B) Yes, user opt-in (Phase 2) | Product Manager | Low |
| **Should admins be able to send custom notifications to tenant users?** | (A) Yes, via admin UI<br>(B) Yes, via API only<br>(C) No, system-generated only | (C) No, system-generated only (add in Phase 3 if requested) | Product Manager | Low |

---

### 14.2 Technical Decisions

| Question | Options | Proposed Default | Stakeholder | Priority |
|----------|---------|------------------|-------------|----------|
| **Should we persist Redis pub/sub messages?** | (A) Yes, use Redis Streams<br>(B) No, ephemeral only | (B) No, ephemeral only | Tech Lead | Medium |
| **Should we implement notification delivery receipts?** | (A) Yes, track delivery confirmation<br>(B) No, assume delivered if sent | (B) No, assume delivered | Tech Lead | Low |
| **Should we batch mark-as-read API calls?** | (A) Yes, debounce by 500ms<br>(B) No, immediate API call per action | (A) Yes, debounce by 500ms | Tech Lead | Medium |
| **Should we implement notification priority levels?** | (A) Yes (high, medium, low)<br>(B) No, all notifications equal priority | (B) No, all equal (add in Phase 3 if needed) | Tech Lead | Low |
| **Should we add notification delivery metrics to telemetry?** | (A) Yes, comprehensive metrics<br>(B) Basic metrics only (count, latency)<br>(C) No metrics | (A) Yes, comprehensive metrics | Tech Lead | High |

---

### 14.3 Compliance & Legal

| Question | Options | Proposed Default | Stakeholder | Priority |
|----------|---------|------------------|-------------|----------|
| **Do notifications contain PII requiring GDPR consent?** | (A) Yes (user names)<br>(B) No | (A) Yes - requires GDPR compliance | Legal | High |
| **Should users be able to export their notification history?** | (A) Yes, required for GDPR<br>(B) No | (A) Yes, add export feature | Legal | High |
| **Should we log who reads which notifications?** | (A) Yes, for audit trail<br>(B) No, privacy concern | (A) Yes, for audit trail (already implemented) | Legal + Security | High |

---

### 14.4 UX/Design

| Question | Options | Proposed Default | Stakeholder | Priority |
|----------|---------|------------------|-------------|----------|
| **Should notification drawer auto-close when user clicks a notification?** | (A) Yes, close drawer<br>(B) No, keep drawer open | (B) No, keep drawer open (better for bulk actions) | UX Designer | Low |
| **Should unread badge show exact count or "9+" for large numbers?** | (A) Exact count (e.g., "47")<br>(B) Capped at 9+ | (B) Capped at 9+ (less overwhelming) | UX Designer | Low |
| **Should we add sound/desktop notifications?** | (A) Yes, with user preference<br>(B) No, visual only | (A) Yes, user opt-in (Phase 2) | UX Designer | Medium |
| **How should grouped notifications be displayed?** | (A) Show count in message "(3) new responses"<br>(B) Show list of items in description | (A) Show count in message (current implementation) | UX Designer | Low |

---

## 15. Revision History

| Version | Date | Author | Summary of Changes |
|---------|------|--------|-------------------|
| 1.0 | 2025-11-12 | Copilot Agent | Initial design document created from developer handover documentation. Includes all sections: architecture, API contracts, database design, security, testing, and implementation plan. |

---

## Appendix A: Notification Format Examples

### In-App Notification Format

**Single Supplier Response:**
```
Message: "(1) new pending responses to approve"
Description: "You have 1 new supplier response to approve in the Campaign Manager module under the Pending Approvals Tab."
Type: info
Timestamp: 2025-11-12T10:30:00Z
```

**Grouped Supplier Responses:**
```
Message: "(5) new pending responses to approve"
Description: "You have 5 new supplier responses to approve in the Campaign Manager module under the Pending Approvals Tab."
Type: info
Timestamp: 2025-11-12T10:35:00Z
Metadata: { count: 5, supplierIds: [...], campaignIds: [...] }
```

**FMD Compliance Status Change:**
```
Message: "Compliance status changed for Battery Cell"
Description: "The compliance status for Battery Cell has been changed from 'Yes' to 'No' by Abhinav Bharadwaj on 12 Nov 2025. Regulation: REACH."
Type: warning
Timestamp: 2025-11-12T10:40:00Z
Metadata: {
  productName: "Battery Cell",
  oldStatus: "Yes",
  newStatus: "No",
  changedBy: "Abhinav Bharadwaj",
  changeDate: "2025-11-12T10:40:00Z",
  regulationType: "REACH"
}
```

**CMRT Supplier Response:**
```
Message: "(3) new pending responses to approve"
Description: "You have 3 new supplier responses (Conflict Minerals) to approve in the Responsible Minerals module under the Response Tracker Tab."
Type: info
GroupId: newSupplierResponseCMRT
Timestamp: 2025-11-12T10:45:00Z
```

---

## Appendix B: Email Notification Format (Future Phase)

### Email Template Design (Planned)

**Subject Line:**
```
Compliance Status Change Notification - [Product Name]
```

**Email Body:**
```html
<html>
<body style="font-family: Arial, sans-serif;">
  <div style="background-color: #f5f5f5; padding: 20px;">
    <h2 style="color: #333;">Compliance Status Change</h2>
    
    <p>Dear User,</p>
    
    <p>The compliance status for <strong>Battery Cell</strong> has changed:</p>
    
    <table style="border-collapse: collapse; margin: 20px 0;">
      <tr>
        <td style="padding: 10px; border: 1px solid #ddd;"><strong>Previous Status:</strong></td>
        <td style="padding: 10px; border: 1px solid #ddd;">Yes</td>
      </tr>
      <tr>
        <td style="padding: 10px; border: 1px solid #ddd;"><strong>New Status:</strong></td>
        <td style="padding: 10px; border: 1px solid #ddd;">No</td>
      </tr>
      <tr>
        <td style="padding: 10px; border: 1px solid #ddd;"><strong>Changed By:</strong></td>
        <td style="padding: 10px; border: 1px solid #ddd;">Abhinav Bharadwaj</td>
      </tr>
      <tr>
        <td style="padding: 10px; border: 1px solid #ddd;"><strong>Date:</strong></td>
        <td style="padding: 10px; border: 1px solid #ddd;">12 Nov 2025</td>
      </tr>
      <tr>
        <td style="padding: 10px; border: 1px solid #ddd;"><strong>Regulation:</strong></td>
        <td style="padding: 10px; border: 1px solid #ddd;">REACH</td>
      </tr>
    </table>
    
    <p>
      <a href="https://app.acquis.com/fmd/component/12345" 
         style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
        View in System
      </a>
    </p>
    
    <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">
    
    <p style="font-size: 12px; color: #666;">
      You received this notification because you are subscribed to compliance alerts for your organization.
      <a href="https://app.acquis.com/settings/notifications">Manage notification preferences</a>
    </p>
  </div>
</body>
</html>
```

---

## Appendix C: Monitoring Dashboard Queries

### Application Insights KQL Queries

**SSE Connection Success Rate:**
```kql
requests
| where name == "GET /notifications"
| summarize 
    Total = count(),
    Success = countif(resultCode == 200),
    Failed = countif(resultCode != 200)
  by bin(timestamp, 5m)
| extend SuccessRate = (Success * 100.0) / Total
| project timestamp, SuccessRate, Total
```

**Notification Delivery Latency:**
```kql
customMetrics
| where name == "notification_delivery_latency_ms"
| summarize 
    p50 = percentile(value, 50),
    p95 = percentile(value, 95),
    p99 = percentile(value, 99)
  by bin(timestamp, 5m)
```

**Active SSE Connections:**
```kql
customMetrics
| where name == "sse_active_connections"
| summarize max(value) by bin(timestamp, 1m), cloud_RoleInstance
| render timechart
```

**Notification Grouping Efficiency:**
```kql
customEvents
| where name == "notification_created"
| extend IsGrouped = tobool(customDimensions["isGrouped"])
| summarize 
    Total = count(),
    Grouped = countif(IsGrouped == true),
    Individual = countif(IsGrouped == false)
  by bin(timestamp, 1h)
| extend GroupingRate = (Grouped * 100.0) / Total
```

---

## Appendix D: Troubleshooting Runbook

### Issue: User Not Receiving Notifications

**Diagnostic Steps:**
1. Check if user is logged in and SSE connection established
   ```bash
   # Check Redis for active connection
   redis-cli -h <host> -p <port> -a <password>
   HGETALL sse:connections:<user_email>
   ```

2. Verify user is in notification's `userIds` array
   ```javascript
   db.notifications.findOne({ userIds: "<user_email>" })
   ```

3. Check Application Insights for SSE errors
   ```kql
   traces
   | where message contains "<user_email>" and severityLevel > 2
   | order by timestamp desc
   | take 20
   ```

4. Verify Redis pub/sub is working
   ```bash
   # Subscribe to notifications channel
   redis-cli -h <host> -p <port> -a <password>
   SUBSCRIBE notifications
   ```

**Common Resolutions:**
- User needs to log out and log back in to re-establish SSE connection
- Check if user's JWT token is expired
- Verify Redis connection is healthy on backend instance
- Check if CDN is routing SSE connections properly

---

### Issue: High Notification Delivery Latency

**Diagnostic Steps:**
1. Check Redis latency
   ```bash
   redis-cli -h <host> -p <port> -a <password> --latency
   ```

2. Check MongoDB query performance
   ```javascript
   db.notifications.find().explain("executionStats")
   ```

3. Check backend CPU/memory usage
   ```bash
   # On backend instance
   top -b -n 1 | head -20
   ```

4. Review Application Insights for slow operations
   ```kql
   dependencies
   | where duration > 1000
   | summarize count() by name, target
   | order by count_ desc
   ```

**Common Resolutions:**
- Add missing database indexes
- Scale up Redis instance tier
- Add more backend instances
- Optimize notification grouping logic

---

**End of Design Document**
