# src/agents/debug_agent_v2.py

import sys
import os
from typing import List, Dict, Any, Optional
from functools import wraps
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Confirm, Prompt
import json
import time
import random
from concurrent.futures import ThreadPoolExecutor, TimeoutError

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.modules.logging_setup import logger
from src.modules.errors import OllamaAgentsError, InputError, DataProcessingError
from src.modules.input import get_user_input
from src.modules.agent_components import (
    analyze_input,
    gather_context,
    retrieve_relevant_knowledge,
    update_agent_knowledge,
    generate_follow_up_questions,
    assess_response_quality
)
from src.modules.slash_commands import handle_slash_command
from src.modules.ddg_search import DDGSearch
from src.modules.kb_graph import update_knowledge_graph, get_related_nodes
from src.modules.causal_reasoning import infer_causal_relationships, analyze_causal_chain
from src.modules.hypothesis_testing import generate_hypotheses, design_experiment
from src.modules.ollama_client import generate_response
from src.modules.save_history import chat_history
from src.modules.agent_tools import find_analogies, detect_contradictions, resolve_contradictions
from src.modules.helper_probabilistic import (
    calculate_probability,
    bayes_theorem,
    monte_carlo_simulation,
    probability_distribution_fit
)
from src.modules.helper_analogy import apply_analogy
from config import DEFAULT_MODEL, AGENT_NAME, USER_NAME

console = Console()
ddg_search = DDGSearch()

def debug_panel(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        console.print(Panel(f"Entering: {func_name}", border_style="green"))
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            console.print(Panel(f"Error in {func_name}: {str(e)}", border_style="red"))
            raise
        finally:
            console.print(Panel(f"Exiting: {func_name}", border_style="yellow"))
    return wrapper

class DebugAgentV2:
    def __init__(self, model_name=DEFAULT_MODEL):
        self.model_name = model_name
        self.config = {
            'DEFAULT_MODEL': model_name,
            'AGENT_NAME': AGENT_NAME,
            'USER_NAME': USER_NAME
        }
        self.conversation_history = []
        self.bullet_points = []
        self.knowledge_graph = {}
        self.last_response = ""
        self.current_goal = None
        self.progress_status = None
        self.ddg_search = DDGSearch()
        self.context = ""

    @debug_panel
    def run(self):
        self._print_welcome_message()
        self._setup_user_profile()
        self._clear_history_prompt()

        while True:
            user_input = self._get_user_input()
            if user_input is None:
                break
            if user_input == 'CONTINUE':
                continue
            if user_input.startswith('/'):
                response = self._handle_command(user_input)
                if response is None:
                    break
            else:
                response = self._process_input(user_input)
            self._output_response(response)

        self._print_farewell_message()

    @debug_panel
    def _print_welcome_message(self):
        console.print(f"🚀 {AGENT_NAME} v2 initialized. I'm your advanced debug AI assistant with enhanced reasoning capabilities. Type '/q' to quit or '/help' for commands.", style="bold green")

    @debug_panel
    def _setup_user_profile(self):
        console.print("Setting up user profile", style="bold blue")
        self.config['expertise_level'] = Prompt.ask("What's your expertise level?", choices=['beginner', 'medium', 'expert'], default="medium")
        interests = Prompt.ask("What are your main interests? (comma-separated)")
        self.config['interests'] = [interest.strip() for interest in interests.split(',')]
        self.config['language_preference'] = Prompt.ask("Preferred language", default="English")
        console.print(f"Profile set up: {self.config}", style="bold green")

    @debug_panel
    def _clear_history_prompt(self):
        if Confirm.ask("Do you want to clear the chat history?"):
            chat_history.clear()
            self.conversation_history.clear()
            self.bullet_points.clear()
            self.knowledge_graph.clear()
            console.print("Chat history and knowledge graph cleared.", style="bold green")

    @debug_panel
    def _get_user_input(self) -> Optional[str]:
        try:
            return get_user_input()
        except Exception as e:
            logger.error(f"Error getting user input: {str(e)}")
            return None

    @debug_panel
    def _handle_command(self, command: str) -> Optional[str]:
        if command.startswith('/probabilistic_assessment'):
            query = command.split(' ', 1)[1]
            assessment = self._perform_probabilistic_assessment(query, self.context, self._retrieve_enhanced_knowledge(self.context, {}))
            return f"Probabilistic Assessment:\n{json.dumps(assessment, indent=2)}"
        elif command.startswith('/apply_analogy'):
            _, source, target = command.split(' ', 2)
            analogy = {'source_concept': source, 'target_concept': target}
            result = self._apply_analogy(analogy, self.context)
            return f"Analogy Application Result:\n{result}"
        else:
            result = handle_slash_command(command)
            if result == 'EXIT':
                return None
            elif result != 'CONTINUE':
                return result

        if command == '/context':
            return f"📚 Current context:\n{self.context}"
        elif command == '/clear_context':
            self.context = ""
            self.bullet_points.clear()
            self.knowledge_graph.clear()
            return "🧹 Context, bullet points, and knowledge graph cleared."
        elif command == '/bullets':
            return self._display_bullet_points()
        elif command == '/graph':
            return self._display_knowledge_graph()
        else:
            return f"❓ Unknown command: {command}. Type '/help' for available commands."

    @debug_panel
    def _process_input(self, user_input: str, max_retries: int = 3, timeout: int = 60) -> str:
        start_time = time.time()
        for attempt in range(max_retries):
            try:
                with ThreadPoolExecutor() as executor:
                    future = executor.submit(self._process_input_core, user_input)
                    try:
                        return future.result(timeout=timeout)
                    except TimeoutError:
                        logger.error(f"Processing timed out after {timeout} seconds")
                        return f"I apologize, but the processing is taking longer than expected. Please try a simpler query or try again later."

            except Exception as e:
                logger.exception(f"Error in attempt {attempt + 1}: {str(e)}")
                if attempt == max_retries - 1:
                    return f"I apologize, but I'm having trouble processing your request. Could you please rephrase or ask a different question?"

            finally:
                end_time = time.time()
                logger.info(f"Processing attempt {attempt + 1} took {end_time - start_time:.2f} seconds")

        return "I'm sorry, but I'm unable to provide a helpful response at this time. Please try again later or contact support."

    def _process_input_core(self, user_input: str) -> str:
        if not self.current_goal:
            self._set_current_goal(user_input)

        analysis = analyze_input(user_input, self.config)
        console.print(Panel(f"Input Analysis: {json.dumps(analysis, indent=2)}", border_style="blue"))

        self.context = self._gather_enhanced_context(user_input, analysis)
        console.print(Panel(f"Gathered Context: {self.context[:500]}...", border_style="blue"))

        knowledge = self._retrieve_enhanced_knowledge(self.context, analysis)
        console.print(Panel(f"Retrieved Knowledge: {json.dumps(knowledge, indent=2)}", border_style="blue"))

        if not knowledge:
            knowledge = self._perform_additional_search(user_input, analysis)
            console.print(Panel(f"Additional Search Results: {json.dumps(knowledge, indent=2)}", border_style="blue"))

        causal_relationships = self._perform_causal_analysis(self.context)

        if "event" in analysis:
            event_causal_chain = self._analyze_event_causal_chain(analysis["event"], self.context)

        hypotheses = self._generate_and_test_hypotheses(self.context)

        analogies = self._find_analogies(user_input, self.context)
        console.print(Panel(f"Found Analogies: {json.dumps(analogies, indent=2)}", border_style="cyan"))

        contradictions = self._detect_and_resolve_contradictions(knowledge)
        console.print(Panel(f"Detected and Resolved Contradictions: {json.dumps(contradictions, indent=2)}", border_style="cyan"))

        probabilistic_assessment = self._perform_probabilistic_assessment(user_input, self.context, knowledge)
        console.print(Panel(f"Probabilistic Assessment: {json.dumps(probabilistic_assessment, indent=2)}", border_style="magenta"))

        plan = self._create_and_analyze_plan(user_input, self.context, knowledge, causal_relationships, hypotheses, analogies, contradictions, probabilistic_assessment)
        console.print(Panel(f"Analyzed Plan:\n{plan}", border_style="cyan"))

        response = self._generate_response_from_plan(plan, user_input, self.context, knowledge, causal_relationships, hypotheses, analogies, contradictions, probabilistic_assessment)

        self._assess_progress(response, plan)

        next_step = self._determine_next_step(plan)
        response += f"\n\nNext step: {next_step}"

        if self._is_ethical_concern(response):
            reframed_query = self._reframe_query(user_input)
            console.print(Panel(f"Reframed Query: {reframed_query}", border_style="yellow"))
            return self._process_input(reframed_query, max_retries=1)

        self._update_conversation_history(user_input, response)
        self._update_knowledge_graph(analysis['topics'], response)
        update_agent_knowledge(response, self.context, self.config)

        quality_score, quality_explanation = assess_response_quality(response, self.context, self.config)
        console.print(f"Response quality: {quality_score:.2f}/1.00 - {quality_explanation}", style="bold cyan")

        self._update_bullet_points(response)

        return response

    @debug_panel
    def _set_current_goal(self, user_input: str):
        goal_prompt = f"Based on the user input: '{user_input}', what is the main goal or objective? Provide a concise statement of the goal."
        self.current_goal = generate_response(goal_prompt, self.model_name, self.config['USER_NAME'])
        console.print(Panel(f"Current Goal: {self.current_goal}", border_style="magenta"))

    @debug_panel
    def _gather_enhanced_context(self, user_input: str, analysis: Dict[str, Any]) -> str:
        context = gather_context(user_input, analysis, self.config)
        for topic in analysis['topics']:
            related_nodes = get_related_nodes(topic)
            if related_nodes:
                context += f"\nRelated information for {topic}:\n"
                for node, relation, strength in related_nodes:
                    context += f"- {node} ({relation}, strength: {strength})\n"
        return context

    @debug_panel
    def _retrieve_enhanced_knowledge(self, context: str, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            refined_query = self._refine_query(context, analysis)
            search_queries = self._generate_search_queries(refined_query)
            all_results = []

            console.print(f"Generated search queries: {json.dumps(search_queries)}")

            for query in search_queries:
                console.print(f"Executing search query: {query}")
                results = self._perform_search(query)
                console.print(f"Found {len(results)} results for '{query}'")
                all_results.extend(results[:3])

            filtered_results = self._filter_and_rank_results(all_results, context)
            return filtered_results
        except Exception as e:
            logger.exception(f"Error in _retrieve_enhanced_knowledge: {str(e)}")
            return []

    @debug_panel
    def _refine_query(self, context: str, analysis: Dict[str, Any]) -> str:
        refine_prompt = f"Given the context: {context}\nAnd the analysis: {analysis}\nRefine the search query to focus on the most relevant aspects."
        return generate_response(refine_prompt, self.model_name, self.config['USER_NAME'])

    @debug_panel
    def _generate_search_queries(self, refined_query: str) -> List[str]:
        generate_prompt = f"""
        Generate 5 specific and focused search queries based on this refined query: {refined_query}
        Provide your response as a JSON array of strings.
        """
        queries_json = generate_response(generate_prompt, self.model_name, self.config['USER_NAME'])
        queries = json.loads(queries_json)
        return queries if isinstance(queries, list) else []

    @debug_panel
    def _perform_search(self, query: str) -> List[Dict[str, Any]]:
        search_results = self.ddg_search.run_search(query)
        return [{"source": "web_search", "content": result} for result in search_results[:3]]

    @debug_panel
    def _filter_and_rank_results(self, results: List[Dict[str, Any]], context: str) -> List[Dict[str, Any]]:
        filter_prompt = f"""Given these search results:\n{results}\nAnd this context:\n{context}\nRank and filter the results based on their relevance. Return only the top 3 most relevant results."""
        filtered_results = generate_response(filter_prompt, self.model_name, self.config['USER_NAME'])
        return json.loads(filtered_results) or []

    @debug_panel
    def _perform_additional_search(self, query: str, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        search_query = " ".join(analysis['topics'])
        search_results = self.ddg_search.run_search(search_query)
        return [{"source": "web_search", "content": result} for result in search_results[:3]]

    @debug_panel
    def _perform_causal_analysis(self, context: str) -> List[Dict[str, Any]]:
        console.print("Performing causal analysis...", style="bold blue")
        causal_relationships = infer_causal_relationships(context, self.model_name)
        console.print(Panel(f"Inferred Causal Relationships:\n{json.dumps(causal_relationships, indent=2)}", border_style="cyan"))
        return causal_relationships

    @debug_panel
    def _analyze_event_causal_chain(self, event: str, context: str) -> Dict[str, Any]:
        console.print(f"Analyzing causal chain for event: {event}", style="bold blue")
        causal_chain = analyze_causal_chain(event, context, self.model_name)
        console.print(Panel(f"Causal Chain Analysis:\n{json.dumps(causal_chain, indent=2)}", border_style="cyan"))
        return causal_chain

    @debug_panel
    def _generate_and_test_hypotheses(self, context: str) -> List[Dict[str, Any]]:
        console.print("Generating hypotheses...", style="bold blue")
        hypotheses = generate_hypotheses(context, self.model_name)
        console.print(Panel(f"Generated Hypotheses:\n{json.dumps(hypotheses, indent=2)}", border_style="cyan"))

        tested_hypotheses = []
        for hypothesis in hypotheses:
            console.print(f"Designing experiment for hypothesis: {hypothesis['hypothesis']}", style="bold blue")
            experiment = design_experiment(hypothesis['hypothesis'], context, self.model_name)
            tested_hypothesis = {**hypothesis, "experiment": experiment}
            tested_hypotheses.append(tested_hypothesis)
            console.print(Panel(f"Experiment Design:\n{json.dumps(experiment, indent=2)}", border_style="cyan"))

        return tested_hypotheses

    @debug_panel
    def _find_analogies(self, problem: str, context: str) -> List[Dict[str, str]]:
        console.print("Finding analogies...", style="bold blue")
        analogies = find_analogies(problem, context, self.model_name)
        return analogies

    @debug_panel
    def _detect_and_resolve_contradictions(self, information: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        console.print("Detecting and resolving contradictions...", style="bold blue")
        information_set = [item['content'] for item in information]
        contradictions = detect_contradictions(information_set, self.model_name)
        resolutions = resolve_contradictions(contradictions, self.model_name)
        return resolutions

    @debug_panel
    def _perform_probabilistic_assessment(self, user_input: str, context: str, knowledge: List[Dict[str, Any]]) -> Dict[str, Any]:
        console.print("Performing probabilistic assessment...", style="bold blue")
        prior_probability = calculate_probability(len(knowledge), 100)  # Assume 100 is the total possible knowledge items
        likelihood = bayes_theorem(prior_probability, 0.8, 0.5)  # Example values

        def simulation_func():
            return random.random() < likelihood

        simulation_results = monte_carlo_simulation(simulation_func, num_simulations=1000)

        dist_name, params = probability_distribution_fit(simulation_results)

        assessment = {
            "prior_probability": prior_probability,
            "likelihood": likelihood,
            "simulation_results": sum(simulation_results) / len(simulation_results),
            "distribution_fit": {
                "name": dist_name,
                "parameters": params
            }
        }
        console.print(Panel(f"Probabilistic Assessment:\n{json.dumps(assessment, indent=2)}", border_style="magenta"))
        return assessment

    @debug_panel
    def _apply_analogy(self, analogy: Dict[str, Any], context: str) -> str:
        console.print("Applying analogy...", style="bold blue")
        result = apply_analogy(analogy['source_concept'], analogy['target_concept'], context)
        console.print(Panel(f"Analogy Application Result:\n{result}", border_style="cyan"))
        return result

    @debug_panel
    def _create_and_analyze_plan(self, user_input: str, context: str, knowledge: List[Dict[str, Any]],
                                 causal_relationships: List[Dict[str, Any]], hypotheses: List[Dict[str, Any]],
                                 analogies: List[Dict[str, str]], contradictions: List[Dict[str, Any]],
                                 probabilistic_assessment: Dict[str, Any]) -> str:
        plan_prompt = f"""
        Based on the user input: "{user_input}"
        And the following context, knowledge, causal relationships, hypotheses, analogies, resolved contradictions, and probabilistic assessment:
        Context: {context}
        Knowledge: {json.dumps(knowledge)}
        Causal Relationships: {json.dumps(causal_relationships)}
        Hypotheses: {json.dumps(hypotheses)}
        Analogies: {json.dumps(analogies)}
        Resolved Contradictions: {json.dumps(contradictions)}
        Probabilistic Assessment: {json.dumps(probabilistic_assessment)}
        Current Goal: {self.current_goal}

        1. Create a structured plan with main steps to address the user's query and achieve the current goal.
        2. For each main step, provide 2-3 sub-steps or considerations.
        3. Analyze the feasibility and potential challenges of each main step.
        4. Include a step to evaluate progress towards the goal.
        5. Incorporate relevant causal relationships, hypotheses, analogies, resolved contradictions, and probabilistic insights into the plan.

        Format your response as a JSON object with the following structure:
        {{
            "main_steps": [
                {{
                    "step": "Step description",
                    "sub_steps": ["Sub-step 1", "Sub-step 2", "Sub-step 3"],
                    "analysis": "Analysis of feasibility and challenges",
                    "progress_indicator": "How to measure progress for this step"
                }},
                ...
            ],
            "overall_progress_evaluation": "Description of how to evaluate overall progress towards the goal"
        }}
        """
        plan_response = generate_response(plan_prompt, self.model_name, self.config['USER_NAME'])
        plan_json = json.loads(plan_response)
        return json.dumps(plan_json, indent=2)

    @debug_panel
    def _generate_response_from_plan(self, plan: str, user_input: str, context: str, knowledge: List[Dict[str, Any]],
                                     causal_relationships: List[Dict[str, Any]], hypotheses: List[Dict[str, Any]],
                                     analogies: List[Dict[str, str]], contradictions: List[Dict[str, Any]],
                                     probabilistic_assessment: Dict[str, Any]) -> str:
        response_prompt = f"""
        Based on the following plan:
        {plan}

        And considering the original user input: "{user_input}"
        As well as the context, knowledge, causal relationships, hypotheses, analogies, resolved contradictions, and probabilistic assessment:
        Context: {context}
        Knowledge: {json.dumps(knowledge)}
        Causal Relationships: {json.dumps(causal_relationships)}
        Hypotheses: {json.dumps(hypotheses)}
        Analogies: {json.dumps(analogies)}
        Resolved Contradictions: {json.dumps(contradictions)}
        Probabilistic Assessment: {json.dumps(probabilistic_assessment)}
        Current Goal: {self.current_goal}

        Generate a comprehensive response that:
        1. Addresses the user's query
        2. Follows the structure of the plan
        3. Incorporates relevant information from the context, knowledge, causal relationships, hypotheses, analogies, resolved contradictions, and probabilistic assessment
        4. Highlights any important considerations or challenges
        5. Evaluates the current progress towards the goal
        6. Suggests the next immediate action to take
        7. Discusses relevant causal relationships and how they impact the plan
        8. Mentions relevant hypotheses and how they could be tested or incorporated into the plan
        9. Utilizes relevant analogies to explain complex concepts or strategies
        10. Addresses any resolved contradictions and explains their impact on the solution
        11. Incorporates insights from the probabilistic assessment to evaluate uncertainties and risks

        Ensure the response is clear, informative, and directly relevant to the user's needs and the current goal.
        """
        return generate_response(response_prompt, self.model_name, self.config['USER_NAME'])

    @debug_panel
    def _assess_progress(self, response: str, plan: str):
        progress_prompt = f"""
        Based on the current response:
        {response}

        And the original plan:
        {plan}

        Evaluate the progress towards the current goal: {self.current_goal}
        Provide a brief status update and a percentage of completion (0-100%).

        Format your response as a JSON object:
        {{
            "status": "Brief status update",
            "completion_percentage": 75
        }}
        """
        progress_response = generate_response(progress_prompt, self.model_name, self.config['USER_NAME'])
        progress_json = json.loads(progress_response)
        if progress_json:
            self.progress_status = progress_json
            console.print(Panel(f"Progress Assessment:\n{json.dumps(progress_json, indent=2)}", border_style="green"))
        else:
            logger.error(f"Failed to parse JSON from progress assessment: {progress_response}")

    @debug_panel
    def _determine_next_step(self, plan: str) -> str:
        next_step_prompt = f"""
        Based on the current plan:
        {plan}

        And the current progress status:
        {json.dumps(self.progress_status)}

        Determine the next immediate step to take to move closer to the goal: {self.current_goal}
        Provide a clear and concise description of the next action.
        """
        return generate_response(next_step_prompt, self.model_name, self.config['USER_NAME'])

    @debug_panel
    def _update_conversation_history(self, user_input: str, response: str):
        self.conversation_history.append({"prompt": user_input, "response": response})
        if len(self.conversation_history) > 10:
            self.conversation_history.pop(0)

    @debug_panel
    def _update_knowledge_graph(self, topics: List[str], response: str):
        for topic in topics:
            update_knowledge_graph(topic, response)

    @debug_panel
    def _update_bullet_points(self, response: str):
        new_points = response.split('\n')
        self.bullet_points.extend([point.strip() for point in new_points if point.strip().startswith('•')])
        self.bullet_points = self.bullet_points[-10:]

    @debug_panel
    def _handle_followup(self, context: str) -> Optional[str]:
        followup_questions = generate_follow_up_questions(context, self.config)
        if followup_questions:
            console.print("📚 Based on our conversation, here are some follow-up questions you might find interesting:", style="bold cyan")
            for i, question in enumerate(followup_questions, 1):
                console.print(f"  {i}. {question}")
            console.print("You can choose a number, ask your own question, or press Enter to skip.")

            choice = console.input("Your choice (number, question, or Enter to skip): ")

            if choice.strip() == "":
                return None
            elif choice.isdigit() and 1 <= int(choice) <= len(followup_questions):
                selected_question = followup_questions[int(choice) - 1]
            else:
                selected_question = choice

            console.print(f"Processing follow-up: {selected_question}", style="bold yellow")
            followup_response = self._process_input(selected_question)
            return f"Follow-up: {selected_question}\n\nResponse: {followup_response}"
        return None

    @debug_panel
    def _output_response(self, response: str):
        console.print(f"🤖 {AGENT_NAME}:", style="bold magenta")
        console.print(response)

    @debug_panel
    def _display_bullet_points(self) -> str:
        if not self.bullet_points:
            return "No bullet points available."
        return "📌 Current key points:\n" + "\n".join(f"• {point}" for point in self.bullet_points)

    @debug_panel
    def _display_knowledge_graph(self) -> str:
        if not self.knowledge_graph:
            return "Knowledge graph is empty."
        return f"🕸️ Knowledge Graph:\n{json.dumps(self.knowledge_graph, indent=2)}"

    @debug_panel
    def _print_farewell_message(self):
        console.print(f"👋 Thank you for using {AGENT_NAME}. Your debug session has ended. Goodbye!", style="bold red")

    def _is_ethical_concern(self, response: str) -> bool:
        concern_phrases = [
            "I can't provide",
            "illegal",
            "unethical",
            "copyright infringement",
            "against the law",
            "not permitted"
        ]
        return any(phrase in response.lower() for phrase in concern_phrases)

    def _reframe_query(self, original_query: str) -> str:
        reframe_prompt = f"""
        The following query may have ethical or legal concerns:
        "{original_query}"
        Please reframe this query to focus on legal and ethical approaches to achieve the same goal.
        Provide only the reframed query, without any additional explanation.
        """
        reframed_query = generate_response(reframe_prompt, self.model_name, self.config['USER_NAME'])
        return reframed_query.strip()

@debug_panel
def run():
    try:
        agent = DebugAgentV2()
        agent.run()
    except Exception as e:
        logger.exception(f"An error occurred in DebugAgentV2: {str(e)}")
        console.print(f"An error occurred: {str(e)}", style="bold red")

def main():
    run()

if __name__ == "__main__":
    main()
