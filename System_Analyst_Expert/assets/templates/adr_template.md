# ADR-XXX: [Short Title of Decision]

**Status:** Proposed | Accepted | Rejected | Deprecated | Superseded  
**Date:** YYYY-MM-DD  
**Author:** [Name]  
**Reviewers:** [Names]

---

## Context

[Describe the problem or opportunity that requires a decision. Include:
- Background information
- Current situation
- Forces at play (technical, business, political, social)
- Constraints
- Requirements that led to this decision]

**Example:**
We need to choose a database for our new user management system. The system will handle 100K+ users with complex relationships (followers, friends, groups). We expect high read traffic (90% reads, 10% writes) and need ACID transactions for payment processing.

---

## Decision

[State the decision clearly and concisely]

**Example:**
We will use PostgreSQL as our primary database for the user management system.

---

## Rationale

[Explain WHY this decision was made. Include:
- Alternatives considered
- Comparison of options (pros/cons)
- Why this option is superior
- Supporting data/research]

**Example:**

### Alternatives Considered:

1. **PostgreSQL** (Selected)
   - ✅ ACID transactions (critical for payments)
   - ✅ Rich query capabilities (complex relationships)
   - ✅ JSON support (flexible user profiles)
   - ✅ Mature ecosystem, excellent documentation
   - ❌ Harder to scale horizontally than NoSQL

2. **MongoDB**
   - ✅ Horizontal scaling out-of-the-box
   - ✅ Flexible schema
   - ❌ No ACID transactions across collections
   - ❌ Complex relationship queries less efficient

3. **DynamoDB**
   - ✅ Fully managed, auto-scaling
   - ✅ Extremely fast reads
   - ❌ Limited query flexibility
   - ❌ Expensive for complex access patterns

### Why PostgreSQL:
- ACID transactions are non-negotiable for payment processing
- Relationship-heavy data model fits relational paradigm
- Team has strong PostgreSQL expertise
- Read scaling achievable with read replicas (sufficient for our scale)

---

## Consequences

[Describe the resulting context after applying the decision. Include:
- Positive consequences (benefits)
- Negative consequences (trade-offs, risks)
- Mitigation strategies for negative consequences
- Impact on other systems/teams]

**Example:**

### Positive:
- Data integrity guaranteed (ACID)
- Complex queries performant with proper indexing
- Rich ecosystem of tools (PgAdmin, pg_stat_statements)
- Easy to hire developers with PostgreSQL experience

### Negative:
- Horizontal scaling more complex than NoSQL
- Requires careful schema design upfront
- Connection pool management needed

### Mitigation:
- Implement read replicas for read scaling
- Use PgBouncer for connection pooling
- Design schema with future partitioning in mind
- Monitor query performance from day one

---

## Related Decisions

- [ADR-005: Choice of ORM](#) - Depends on this decision
- [ADR-012: Caching Strategy](#) - Complements this decision

---

## Notes

[Optional section for additional context, updates, or references]

**References:**
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Benchmark Study: PostgreSQL vs MongoDB](https://example.com)

**Updates:**
- YYYY-MM-DD: Decision status changed to Accepted
- YYYY-MM-DD: Added note about read replica strategy

---

## Template Guidelines

### When to Create an ADR

Create an ADR for decisions that:
- Have long-term impact on the system
- Are difficult or expensive to reverse
- Affect multiple teams or components
- Require justification for stakeholders

### Good ADR Characteristics

1. **Clear Context**: Anyone reading should understand the problem
2. **Explicit Decision**: No ambiguity about what was decided
3. **Documented Rationale**: Future readers understand WHY
4. **Honest Consequences**: Both positives and negatives acknowledged
5. **Timely**: Written when the decision is fresh

### ADR Lifecycle

- **Proposed**: Under discussion
- **Accepted**: Decision approved and implemented
- **Rejected**: Decision not approved
- **Deprecated**: Superseded by a newer decision
- **Superseded**: Replaced by ADR-XXX

### Numbering Convention

- Sequential numbering: ADR-001, ADR-002, ADR-003...
- Never reuse numbers
- Include number in filename: `ADR-001-database-selection.md`

---

**Template Version:** 1.0  
**Last Updated:** 2025-01-12
