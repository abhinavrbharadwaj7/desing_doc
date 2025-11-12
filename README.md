# Design Documents Repository

This repository contains technical design documents for various systems and features.

## Available Design Documents

### [FMD Notification System](./FMD_Notification_System_Design.md)

A comprehensive design document for the Full Material Disclosure (FMD) Notification System - a real-time, scalable notification solution for the Acquis Compliance Platform.

**Quick Links:**
- [Overview & Scope](./FMD_Notification_System_Design.md#2-overview)
- [System Architecture](./FMD_Notification_System_Design.md#5-system-architecture)
- [API Contracts](./FMD_Notification_System_Design.md#7-api-contracts)
- [Implementation Timeline](./FMD_Notification_System_Design.md#11-implementation-plan--timeline)
- [Testing Strategy](./FMD_Notification_System_Design.md#12-testing--validation)

**Key Features:**
- Real-time in-app notifications via Server-Sent Events (SSE)
- Multi-tenant isolation with tenant-specific databases
- Horizontal scalability across Azure CDN instances
- Intelligent notification grouping (5-minute window)
- Redis pub/sub for cross-instance communication
- Comprehensive security and compliance (GDPR, SOC 2)

**Status:** Phase 1 Complete | Phase 2 (Email) Planned Q1 2026

---

### [Customer Request Manager (CRM)](./CRM_Design_Document.md)

A comprehensive design document for the Customer Request Manager (CRM) - a centralized platform for tracking and managing customer compliance and sustainability requests with role-based access control.

**Quick Links:**
- [Key Features & Business Rules](./CRM_Design_Document.md#4-key-features--business-rules)
- [Overview & Scope](./CRM_Design_Document.md#2-overview)
- [System Architecture](./CRM_Design_Document.md#5-system-architecture)
- [API Contracts](./CRM_Design_Document.md#7-api-contracts)
- [Implementation Timeline](./CRM_Design_Document.md#11-implementation-plan--timeline)
- [Testing Strategy](./CRM_Design_Document.md#12-testing--validation)

**Key Features:**
- **Role-Based Access Control:** Managers (full access) and Users (assigned tasks only)
- **Centralized request tracking** replacing manual email/Excel methods
- **Real-time dashboards** with KPIs and visual analytics (FusionCharts)
- **Regulatory heat map** for resource planning and optimization (RoHS, REACH, TSCA PBT, Prop 65, Conflict Minerals, FMD)
- **Automated business rules:** Mandatory cancellation reasons, overdue flagging, status transitions
- **File upload/management** with Azure Blob Storage (uflpa container)
- **Comprehensive audit logging** with role tracking
- **Export capabilities** (CSV/Excel) with role-based filtering
- **Smart request form** with dropdowns, calendar pickers, and validation

**Status:** R1 In Progress (Week 3-4 of 8) | R2 Enhancements Planned Q1 2026

---

## Document Structure

All design documents in this repository follow a standardized template including:

1. **Summary** - Executive overview with key outcomes
2. **Overview** - Purpose, scope, and success metrics
3. **Key Definitions** - Technical terminology
4. **Proposed Design** - User flows and components
5. **System Architecture** - Detailed technical design
6. **Database Design** - Schema and data models
7. **API Contracts** - Endpoint specifications
8. **Failure Scenarios** - Risk mitigation strategies
9. **Security & Privacy** - Threat model and compliance
10. **Non-Functional Requirements** - Performance, scalability, monitoring
11. **Implementation Plan** - Timeline and milestones
12. **Testing & Validation** - Quality assurance strategy
13. **Recommendations & Trade-offs** - Decision rationale
14. **Open Questions** - Unresolved decisions
15. **Revision History** - Change tracking
16. **Appendices** - Supporting materials

---

## Using These Documents

### For Engineers
- Reference architecture diagrams and component descriptions
- Use API contracts for implementation
- Follow testing strategies for quality assurance
- Consult troubleshooting runbooks for production issues

### For Product Managers
- Review overview and scope sections
- Understand implementation timeline and phases
- Consider open questions requiring stakeholder input
- Track success metrics and SLA commitments

### For Stakeholders
- Read summary for quick understanding
- Review recommendations and trade-offs for decision-making
- Understand resource requirements and dependencies
- Track revision history for change management

### For Security/Compliance Teams
- Audit security and privacy sections
- Review threat models and mitigations
- Verify compliance requirements (GDPR, SOC 2)
- Assess data encryption and access controls

---

## Contributing

When adding new design documents:

1. Follow the standardized template structure
2. Include comprehensive diagrams (architecture, sequence, ER)
3. Document all API contracts with examples
4. Address security, privacy, and compliance
5. Define clear success metrics and SLAs
6. Include testing strategy and acceptance criteria
7. Add revision history with version tracking

---

## Repository Structure

```
├── README.md                               # This file
├── FMD_Notification_System_Design.md       # FMD notification system design doc
├── CRM_Design_Document.md                  # Customer Request Manager design doc
└── .github/
    └── agents/
        └── my-agent.agent.md               # ProjectDesignDoc-Agent configuration
```

---

## Contact

For questions or feedback about these design documents, please contact the engineering team or create an issue in this repository.
