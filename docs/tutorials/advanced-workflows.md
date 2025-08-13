# Advanced Workflows Tutorial

Complete guide to creating and using advanced analysis workflows in SNID SAGE for complex research projects.

## What are Advanced Workflows?

Advanced workflows enable:
- **Complex multi-step analysis** with conditional logic
- **Automated decision making** based on results
- **Custom processing pipelines** for specific research needs
- **Integration with external tools** and databases
- **Reproducible research** with version-controlled workflows

## Prerequisites

### **Advanced Knowledge**
- Familiarity with SNID SAGE basics
- Understanding of supernova types and features
- Experience with CLI and configuration
- Basic programming concepts

### **Required Tools**
- SNID SAGE installed and configured
- Sample data for testing workflows
- Text editor for workflow configuration
- Understanding of YAML/JSON formats

---

## Part 1: Workflow Fundamentals

### Batch processing

SNID SAGE supports batch processing via the CLI to analyze multiple spectra in one go. See examples:

```powershell
snid batch "data/*.dat" templates/ --output-dir results/
```

### **Workflow Structure**

#### **Basic Workflow Components**
```yaml
workflow:
  name: "Advanced Analysis Workflow"
  version: "1.0"
  description: "Complex analysis pipeline for research"
  
  inputs:
    - spectrum_file: "Path to input spectrum"
    - parameters: "Analysis parameters"
  
  steps:
    - step_name:
        action: "action_type"
        parameters: {}
        conditions: {}
        outputs: {}
  
  outputs:
    - results: "Analysis results"
    - plots: "Generated plots"
    - reports: "Analysis reports"
```

#### **Workflow Types**
```yaml
Workflow Categories:
  - Discovery: New object analysis
  - Research: Detailed investigation
  - Publication: Publication preparation
  - Quality Control: Data quality assessment
  - Batch Processing: Multiple object analysis
  - Custom: User-defined workflows
```

### **Workflow Configuration**

#### **Basic Workflow File**
```yaml
# basic_workflow.yaml
workflow:
  name: "Basic Analysis Workflow"
  version: "1.0"
  
  steps:
    - data_validation:
        action: "validate_data"
        parameters:
          min_snr: 10
          min_coverage: 0.8
        outputs:
          validation_report: "validation.txt"
    
    - preprocessing:
        action: "preprocess"
        parameters:
          smoothing: true
          outlier_removal: true
        outputs:
          processed_spectrum: "processed.dat"
    
    - analysis:
        action: "identify"
        parameters:
          types: ["Ia", "Ib", "Ic", "II"]
          complete: true
        outputs:
          results: "results.json"
    
    - quality_assessment:
        action: "assess_quality"
        parameters:
          min_confidence: 7.0
        outputs:
          quality_report: "quality.txt"
```

#### **Workflow Execution**
```bash
# Execute basic workflow
python run_snid_cli.py workflow basic_workflow.yaml \
    --input spectrum.dat \
    --output-dir workflow_results/

# Execute with custom parameters
python run_snid_cli.py workflow basic_workflow.yaml \
    --input spectrum.dat \
    --parameters "min_snr=15,min_confidence=8.0" \
    --output-dir workflow_results/
```

---

## Part 2: Conditional Workflows

### **Conditional Logic**

#### **Conditional Workflow Structure**
```yaml
# conditional_workflow.yaml
workflow:
  name: "Conditional Analysis Workflow"
  version: "1.0"
  
  steps:
    - initial_analysis:
        action: "identify"
        parameters:
          types: ["Ia", "Ib", "Ic", "II"]
        outputs:
          results: "initial_results.json"
    
    - check_quality:
        action: "check_condition"
        parameters:
          condition: "confidence > 8.0"
        outputs:
          high_quality: "high_quality_flag"
    
    - high_quality_analysis:
        action: "detailed_analysis"
        parameters:
          detailed: true
          ai_analysis: true
        condition: "high_quality == true"
        outputs:
          detailed_results: "detailed_results.json"
    
    - low_quality_analysis:
        action: "basic_analysis"
        parameters:
          basic: true
        condition: "high_quality == false"
        outputs:
          basic_results: "basic_results.json"
```

#### **Conditional Execution**
```bash
# Execute conditional workflow
python run_snid_cli.py workflow conditional_workflow.yaml \
    --input spectrum.dat \
    --output-dir conditional_results/

# Monitor conditional execution
python run_snid_cli.py workflow conditional_workflow.yaml \
    --input spectrum.dat \
    --output-dir conditional_results/ \
    --monitor
```

### **Advanced Conditions**

#### **Complex Conditional Logic**
```yaml
# complex_conditional_workflow.yaml
workflow:
  name: "Complex Conditional Workflow"
  version: "1.0"
  
  steps:
    - initial_analysis:
        action: "identify"
        outputs:
          results: "initial_results.json"
    
    - evaluate_conditions:
        action: "evaluate_conditions"
        parameters:
          conditions:
            - "confidence > 9.0 and snr > 20"
            - "confidence > 7.0 and snr > 15"
            - "confidence > 5.0 and snr > 10"
        outputs:
          quality_level: "quality_level"
    
    - premium_analysis:
        action: "premium_analysis"
        condition: "quality_level == 'premium'"
        outputs:
          results: "premium_results.json"
    
    - standard_analysis:
        action: "standard_analysis"
        condition: "quality_level == 'standard'"
        outputs:
          results: "standard_results.json"
    
    - basic_analysis:
        action: "basic_analysis"
        condition: "quality_level == 'basic'"
        outputs:
          results: "basic_results.json"
```

---

## Part 3: Multi-Step Workflows

### **Sequential Processing**

#### **Sequential Workflow**
```yaml
# sequential_workflow.yaml
workflow:
  name: "Sequential Analysis Workflow"
  version: "1.0"
  
  steps:
    - data_preparation:
        action: "prepare_data"
        parameters:
          normalize: true
          smooth: true
        outputs:
          prepared_data: "prepared.dat"
    
    - initial_classification:
        action: "identify"
        parameters:
          types: ["Ia", "Ib", "Ic", "II"]
        outputs:
          classification: "classification.json"
    
    - type_specific_analysis:
        action: "type_analysis"
        parameters:
          use_classification: true
        outputs:
          type_results: "type_analysis.json"
    
    - feature_analysis:
        action: "analyze_features"
        parameters:
          features: ["Si II 6355", "Ca II H&K", "H-alpha"]
        outputs:
          feature_results: "features.json"
    
    - velocity_analysis:
        action: "analyze_velocity"
        parameters:
          lines: ["Si II 6355", "Ca II H&K"]
        outputs:
          velocity_results: "velocity.json"
    
    - final_synthesis:
        action: "synthesize_results"
        parameters:
          combine_all: true
        outputs:
          final_results: "final_results.json"
```

#### **Parallel Processing**

#### **Parallel Workflow**
```yaml
# parallel_workflow.yaml
workflow:
  name: "Parallel Analysis Workflow"
  version: "1.0"
  
  steps:
    - data_preparation:
        action: "prepare_data"
        outputs:
          prepared_data: "prepared.dat"
    
    - parallel_analyses:
        parallel: true
        steps:
          - template_analysis:
              action: "template_analysis"
              outputs:
                template_results: "template.json"
          
          - feature_analysis:
              action: "feature_analysis"
              outputs:
                feature_results: "features.json"
          
          - statistical_analysis:
              action: "statistical_analysis"
              outputs:
                statistical_results: "stats.json"
    
    - result_combination:
        action: "combine_results"
        parameters:
          wait_for: ["template_analysis", "feature_analysis", "statistical_analysis"]
        outputs:
          combined_results: "combined.json"
```

---

## Part 4: Specialized Workflows

### **Discovery Workflow**

#### **Discovery Pipeline**
```yaml
# discovery_workflow.yaml
workflow:
  name: "Discovery Analysis Workflow"
  version: "1.0"
  
  steps:
    - quick_assessment:
        action: "quick_analysis"
        parameters:
          fast: true
          basic_types: true
        outputs:
          quick_results: "quick.json"
    
    - quality_check:
        action: "check_quality"
        parameters:
          min_snr: 5
          min_coverage: 0.5
        outputs:
          quality_flag: "quality.txt"
    
    - detailed_analysis:
        action: "detailed_analysis"
        condition: "quality_flag == 'good'"
        parameters:
          complete: true
          ai_analysis: true
        outputs:
          detailed_results: "detailed.json"
    
    - alert_generation:
        action: "generate_alert"
        condition: "quality_flag == 'good'"
        parameters:
          alert_type: "discovery"
        outputs:
          alert: "alert.txt"
    
    - follow_up_planning:
        action: "plan_followup"
        condition: "quality_flag == 'good'"
        outputs:
          followup_plan: "followup.txt"
```

### **Research Workflow**

#### **Research Pipeline**
```yaml
# research_workflow.yaml
workflow:
  name: "Research Analysis Workflow"
  version: "1.0"
  
  steps:
    - comprehensive_analysis:
        action: "comprehensive_analysis"
        parameters:
          all_methods: true
          detailed: true
        outputs:
          comprehensive_results: "comprehensive.json"
    
    - statistical_analysis:
        action: "statistical_analysis"
        parameters:
          confidence_intervals: true
          uncertainty_analysis: true
        outputs:
          statistical_results: "statistics.json"
    
    - literature_comparison:
        action: "literature_comparison"
        parameters:
          database: "simbad"
          papers: true
        outputs:
          literature_results: "literature.json"
    
    - physical_interpretation:
        action: "physical_interpretation"
        parameters:
          models: true
          parameters: true
        outputs:
          interpretation: "interpretation.txt"
    
    - publication_preparation:
        action: "prepare_publication"
        parameters:
          figures: true
          tables: true
          text: true
        outputs:
          publication: "publication/"
```

### **Quality Control Workflow**

#### **Quality Control Pipeline**
```yaml
# quality_control_workflow.yaml
workflow:
  name: "Quality Control Workflow"
  version: "1.0"
  
  steps:
    - data_validation:
        action: "validate_data"
        parameters:
          comprehensive: true
        outputs:
          validation_report: "validation.txt"
    
    - quality_assessment:
        action: "assess_quality"
        parameters:
          metrics: ["snr", "coverage", "calibration"]
        outputs:
          quality_report: "quality.txt"
    
    - outlier_detection:
        action: "detect_outliers"
        parameters:
          method: "statistical"
        outputs:
          outliers: "outliers.txt"
    
    - quality_improvement:
        action: "improve_quality"
        parameters:
          methods: ["smoothing", "calibration"]
        outputs:
          improved_data: "improved.dat"
    
    - final_validation:
        action: "final_validation"
        parameters:
          standards: true
        outputs:
          final_report: "final_validation.txt"
```

---

## Part 5: Iterative Workflows

### **Iterative Processing**

#### **Iterative Workflow**
```yaml
# iterative_workflow.yaml
workflow:
  name: "Iterative Analysis Workflow"
  version: "1.0"
  
  steps:
    - initial_analysis:
        action: "identify"
        parameters:
          types: ["Ia", "Ib", "Ic", "II"]
        outputs:
          initial_results: "initial.json"
    
    - quality_evaluation:
        action: "evaluate_quality"
        parameters:
          threshold: 7.0
        outputs:
          quality_score: "quality.txt"
    
    - iterative_improvement:
        action: "iterative_improvement"
        parameters:
          max_iterations: 5
          improvement_threshold: 0.1
        condition: "quality_score < 8.0"
        outputs:
          improved_results: "improved.json"
    
    - final_analysis:
        action: "final_analysis"
        parameters:
          best_methods: true
        outputs:
          final_results: "final.json"
```

### **Convergence Workflows**

#### **Convergence Pipeline**
```yaml
# convergence_workflow.yaml
workflow:
  name: "Convergence Analysis Workflow"
  version: "1.0"
  
  steps:
    - multiple_analyses:
        action: "multiple_analyses"
        parameters:
          methods: ["template", "feature", "statistical"]
        outputs:
          method_results: "methods/"
    
    - convergence_check:
        action: "check_convergence"
        parameters:
          tolerance: 0.01
          max_iterations: 10
        outputs:
          convergence_flag: "convergence.txt"
    
    - result_synthesis:
        action: "synthesize_results"
        parameters:
          weighted_average: true
        outputs:
          synthesized_results: "synthesized.json"
```

---

## Part 6: External Integration

### **Database Integration**

#### **Database Workflow**
```yaml
# database_workflow.yaml
workflow:
  name: "Database Integration Workflow"
  version: "1.0"
  
  steps:
    - analysis:
        action: "identify"
        outputs:
          results: "results.json"
    
    - database_query:
        action: "query_database"
        parameters:
          database: "simbad"
          query_type: "similar_objects"
        outputs:
          database_results: "database.json"
    
    - comparison:
        action: "compare_results"
        parameters:
          internal: "results.json"
          external: "database.json"
        outputs:
          comparison: "comparison.txt"
    
    - database_update:
        action: "update_database"
        parameters:
          database: "local"
          update_type: "append"
        outputs:
          update_report: "update.txt"
```

### **External Tool Integration**

#### **External Tool Workflow**
```yaml
# external_tool_workflow.yaml
workflow:
  name: "External Tool Integration Workflow"
  version: "1.0"
  
  steps:
    - snid_analysis:
        action: "identify"
        outputs:
          snid_results: "snid.json"
    
    - external_analysis:
        action: "external_tool"
        parameters:
          tool: "custom_analysis_script.py"
          parameters: "--input {snid_results}"
        outputs:
          external_results: "external.json"
    
    - result_combination:
        action: "combine_results"
        parameters:
          sources: ["snid_results", "external_results"]
        outputs:
          combined_results: "combined.json"
```

---

## Part 7: Workflow Monitoring

### **Progress Tracking**

#### **Monitoring Configuration**
```yaml
# monitored_workflow.yaml
workflow:
  name: "Monitored Analysis Workflow"
  version: "1.0"
  
  monitoring:
    enabled: true
    progress_tracking: true
    resource_monitoring: true
    error_tracking: true
  
  steps:
    - analysis:
        action: "identify"
        monitoring:
          progress: true
          resources: true
        outputs:
          results: "results.json"
```

#### **Monitoring Commands**
```bash
# Monitor workflow execution
python run_snid_cli.py workflow monitored_workflow.yaml \
    --input spectrum.dat \
    --monitor \
    --output-dir monitored_results/

# Check workflow status
python run_snid_cli.py workflow status workflow_id \
    --output status_report.txt

# Monitor resources
python run_snid_cli.py workflow monitor workflow_id \
    --resources \
    --output resource_usage.txt
```

### **Error Handling**

#### **Error Handling Workflow**
```yaml
# error_handling_workflow.yaml
workflow:
  name: "Error Handling Workflow"
  version: "1.0"
  
  error_handling:
    continue_on_error: true
    retry_failed: true
    max_retries: 3
    error_log: "error.log"
  
  steps:
    - analysis:
        action: "identify"
        error_handling:
          retry: true
          fallback: "basic_analysis"
        outputs:
          results: "results.json"
```

---

## Part 8: Workflow Optimization

### **Performance Optimization**

#### **Optimized Workflow**
```yaml
# optimized_workflow.yaml
workflow:
  name: "Optimized Analysis Workflow"
  version: "1.0"
  
  optimization:
    parallel_processing: true
    memory_optimization: true
    caching: true
    resource_limits:
      max_memory: "8GB"
      max_cpu: 4
  
  steps:
    - parallel_analyses:
        parallel: true
        optimization:
          memory_efficient: true
        steps:
          - analysis1:
              action: "analysis_type_1"
          - analysis2:
              action: "analysis_type_2"
```

### **Resource Management**

#### **Resource Management Workflow**
```yaml
# resource_management_workflow.yaml
workflow:
  name: "Resource Management Workflow"
  version: "1.0"
  
  resource_management:
    memory_limit: "4GB"
    cpu_limit: 2
    disk_limit: "10GB"
    timeout: 3600
  
  steps:
    - analysis:
        action: "identify"
        resource_limits:
          memory: "2GB"
          cpu: 1
          timeout: 1800
        outputs:
          results: "results.json"
```

---

## Part 9: Workflow Analytics

### **Performance Analytics**

#### **Analytics Workflow**
```yaml
# analytics_workflow.yaml
workflow:
  name: "Analytics Workflow"
  version: "1.0"
  
  analytics:
    enabled: true
    metrics: ["execution_time", "resource_usage", "accuracy"]
    reporting: true
  
  steps:
    - analysis:
        action: "identify"
        analytics:
          track_performance: true
          track_accuracy: true
        outputs:
          results: "results.json"
    
    - analytics_report:
        action: "generate_analytics"
        parameters:
          report_type: "comprehensive"
        outputs:
          analytics_report: "analytics.txt"
```

### **Workflow Comparison**

#### **Comparison Workflow**
```yaml
# comparison_workflow.yaml
workflow:
  name: "Workflow Comparison"
  version: "1.0"
  
  steps:
    - workflow1:
        action: "execute_workflow"
        parameters:
          workflow: "workflow1.yaml"
        outputs:
          results1: "results1.json"
    
    - workflow2:
        action: "execute_workflow"
        parameters:
          workflow: "workflow2.yaml"
        outputs:
          results2: "results2.json"
    
    - comparison:
        action: "compare_workflows"
        parameters:
          workflows: ["results1", "results2"]
        outputs:
          comparison_report: "comparison.txt"
```

---

## Part 10: Troubleshooting

### **Common Issues**

#### **Workflow Errors**
```bash
# Debug workflow errors
python run_snid_cli.py workflow debug workflow.yaml \
    --input spectrum.dat \
    --output debug_report.txt

# Validate workflow
python run_snid_cli.py workflow validate workflow.yaml \
    --output validation_report.txt
```

#### **Performance Issues**
```bash
# Profile workflow performance
python run_snid_cli.py workflow profile workflow.yaml \
    --input spectrum.dat \
    --output profile_report.txt

# Optimize workflow
python run_snid_cli.py workflow optimize workflow.yaml \
    --output optimized_workflow.yaml
```

### **Recovery Procedures**

#### **Workflow Recovery**
```bash
# Recover from failure
python run_snid_cli.py workflow recover workflow_id \
    --output-dir recovered_results/

# Resume workflow
python run_snid_cli.py workflow resume workflow_id \
    --checkpoint checkpoint.json
```

---

## Best Practices

### **Workflow Design**

#### **Design Guidelines**
1. **Modular design**: Break workflows into logical steps
2. **Error handling**: Include proper error handling
3. **Monitoring**: Add monitoring and logging
4. **Documentation**: Document workflow purpose and usage
5. **Testing**: Test workflows with sample data

#### **Performance Guidelines**
1. **Optimize resources**: Use appropriate resource limits
2. **Parallel processing**: Use parallel processing when possible
3. **Caching**: Enable caching for repeated operations
4. **Efficient algorithms**: Use efficient analysis methods
5. **Resource monitoring**: Monitor resource usage

### **Maintenance**

#### **Maintenance Guidelines**
1. **Version control**: Use version control for workflows
2. **Regular updates**: Update workflows as needed
3. **Performance monitoring**: Monitor workflow performance
4. **Error tracking**: Track and fix errors
5. **Documentation updates**: Keep documentation current

---

## Future Developments

### **Planned Features**

#### **Advanced Workflows**
- **Machine learning**: ML-powered workflow optimization
- **Automated workflow generation**: AI-generated workflows
- **Real-time workflows**: Live data processing workflows
- **Distributed workflows**: Multi-machine workflows

#### **Enhanced Integration**
- **Cloud integration**: Cloud-based workflow execution
- **Database integration**: Enhanced database connectivity
- **External tool integration**: More external tool support
- **API integration**: REST API for workflows

---

## Support & Resources

### **Documentation**
- **[Basic Analysis](basic-analysis.md)** - Basic analysis tutorial
- **[Configuration Guide](../reference/configuration-guide.md)** - Configuration options
- **[CLI Reference](../cli/command-reference.md)** - CLI documentation

### **Tools & Utilities**
```bash
# Workflow commands
python run_snid_cli.py workflow --help

# Workflow management
python run_snid_cli.py workflow manage --help

# Workflow monitoring
python run_snid_cli.py workflow monitor --help
```

### **Community Support**
- **GitHub Issues**: Report workflow problems
- **Discussions**: Workflow-related questions
- **Contributions**: Submit workflow improvements
- **Feedback**: Workflow feature suggestions

---

## References

### **Key Publications**
- **Workflow Systems**: Scientific workflow methodologies
- **Automation**: Scientific automation techniques
- **Reproducible Research**: Reproducible research practices

### **Resources**
- **Workflow Engines**: Scientific workflow engines
- **Automation Tools**: Scientific automation tools
- **Best Practices**: Workflow best practices

For more information, see:
- **[Basic Analysis](basic-analysis.md)** - Basic analysis tutorial
- **[Configuration Guide](../reference/configuration-guide.md)** - Configuration options
- **[CLI Reference](../cli/command-reference.md)** - CLI documentation 