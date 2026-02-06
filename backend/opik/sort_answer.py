import opik
from opik.evaluation.metrics import AnswerRelevance
from dotenv import load_dotenv

load_dotenv()

def get_best_trace_by_relevance(project_name: str, user_question: str):
    """
    Search traces with filters, evaluate with AnswerRelevance, 
    and return the output of the trace with highest relevance score.
    """
    
    # Initialize Opik client
    opik_client = opik.Opik()

    filter_query = 'name contains "final_response"'
    
    # Search traces with two filters
    traces = opik_client.search_traces(
        project_name=project_name,
        filter_string=filter_query,
        max_results=50  
    )
    
    if not traces:
        print("No traces found matching the filters")
        return None
    
    print(f"Found {len(traces)} traces matching filters")
    

    answer_relevance = AnswerRelevance(
        require_context=False,
        model="mistral/mistral-medium-latest"
    )
    
    best_trace = None
    best_score = -1
    trace_scores = []
    
    for trace in traces:
        try:

            if hasattr(trace, 'output') and trace.output:

                if isinstance(trace.output, dict):
                    output_text = trace.output.get('response', str(trace.output))
                else:
                    output_text = str(trace.output)
                
                # Score the trace output against the user question
                score_result = answer_relevance.score(
                    input=user_question,
                    output=output_text
                )
                
                relevance_score = score_result.value
                
                print(f"Trace ID: {trace.id}")
                print(f"Relevance Score: {relevance_score}")
                print(f"Reason: {score_result.reason}")
                print(f"Output: {output_text[:100]}...")
                print("---")
                
                # Track the best scoring trace
                trace_scores.append({
                    'trace': trace,
                    'score': relevance_score,
                    'output': output_text,
                    'reason': score_result.reason
                })
                
                if relevance_score > best_score:
                    best_score = relevance_score
                    best_trace = trace
                    
        except Exception as e:
            print(f"Error evaluating trace {trace.id}: {e}")
            continue
    
    if best_trace:
        print(f"\n🏆 Best trace found!")
        print(f"Trace ID: {best_trace.id}")
        print(f"Best Relevance Score: {best_score}")
        
        if isinstance(best_trace.output, dict):
            return best_trace.output.get('response', str(best_trace.output))
        else:
            return str(best_trace.output)
    else:
        print("No valid traces found for evaluation")
        return None

if __name__ == "__main__":
    project_name = "LLM_DEBATE"  
    user_question = "Why youtube such a big streaming platform?"
    
    best_output = get_best_trace_by_relevance(project_name, user_question)
    
    if best_output:
        print(f"\n📝 Best Answer:")
        print(best_output)
    else:
        print("No suitable answer found")
