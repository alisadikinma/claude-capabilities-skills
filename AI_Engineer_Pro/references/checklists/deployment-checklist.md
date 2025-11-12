# Deployment Checklist

## Pre-Deployment

- [ ] Model tested on representative data
- [ ] Inference latency acceptable (<100ms target)
- [ ] Model optimized (ONNX/quantization)
- [ ] API endpoints defined
- [ ] Input validation implemented
- [ ] Error handling complete
- [ ] Health check endpoint added
- [ ] Load testing performed
- [ ] Documentation written

## Security

- [ ] Authentication/authorization configured
- [ ] Rate limiting enabled
- [ ] Input sanitization implemented
- [ ] HTTPS enabled
- [ ] API keys secured (not in code)
- [ ] Secrets management configured

## Monitoring

- [ ] Logging configured (errors, predictions)
- [ ] Metrics tracking setup (latency, throughput)
- [ ] Alerting configured (downtime, errors)
- [ ] Dashboard created (Grafana/similar)
- [ ] Data drift monitoring planned

## Production

- [ ] Environment variables set
- [ ] Database connections tested
- [ ] Backup strategy defined
- [ ] Rollback plan documented
- [ ] On-call rotation established
- [ ] Load balancing configured
- [ ] Auto-scaling rules defined

## Post-Deployment

- [ ] Monitor first 24 hours closely
- [ ] Review error logs daily
- [ ] Track model performance metrics
- [ ] Collect user feedback
- [ ] Plan retraining cadence
