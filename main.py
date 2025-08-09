# from agents import (Agent, Runner, trace, input_guardrail, GuardrailFunctionOutput, InputGuardrailTripwireTriggered)
# from connection import config
# import asyncio
# import rich
# from pydantic import BaseModel

# # Output model for class timing agent
# class StudentOutput(BaseModel):
#     response: str
#     isTimingChanged: bool

# # Guard agent to handle input checking
# class_timing_guard = Agent(
#     name="Class Timing Guard",
#     instructions="""
#     Your task is to detect if a student is trying to change class timings.
#     If the input contains 'change my class timings' or crying emoji 😭,
#     trigger a guardrail violation.
#     """,
#     output_type=StudentOutput
# )

# # Guardrail function
# @input_guardrail
# async def timing_input_guard(ctx, agent, input):
#     if "change my class timings" in input.lower() or "😭" in input:
#         return GuardrailFunctionOutput(
#             output_info="Changing class timings is not allowed.",
#             tripwire_triggered=True
#         )

#     result = await Runner.run(class_timing_guard, input, run_config=config)
#     rich.print(result.final_output)

#     return GuardrailFunctionOutput(
#         output_info=result.final_output.response,
#         tripwire_triggered=result.final_output.isTimingChanged
#     )


# # Main student-facing agent
# student_agent = Agent(
#     name="Student Agent",
#     instructions="You are a student. Ask questions related to your course.",
#     input_guardrails=[timing_input_guard]
# )

# # Run everything inside main
# async def main():
#     with trace("Input Guardrails"):
#         try:
#             result = await Runner.run(student_agent, "I want to change my class timings 😭😭", run_config=config)
#             # Query:  when is my class timing
#             # Query:I want to change my class timings 😭😭
#             print("Request accepted:", result.final_output)

#         except InputGuardrailTripwireTriggered:
#             print('⚠️ InputGuardRailTripwireTriggered: You are not allowed to change class timings.')



# # Run main with asyncio
# if __name__ == "__main__":
#     asyncio.run(main())

#################################################### Exercise 2 #################################################################
# Exercise #2 Objective: Make a father agent and father guardrail. The father stopping his child to run below 26C.

# from agents import (Agent, Runner, trace, input_guardrail, GuardrailFunctionOutput, InputGuardrailTripwireTriggered)
# from connection import config
# import asyncio
# import rich
# from pydantic import BaseModel

# # Output model for Father Agent
# class RunOutput(BaseModel):
#     response: str
#     canRun: bool

# # Father Guard agent — final decision maker
# father_guard = Agent(
#     name="Father Guard",
#     instructions="""
#     You are a father. The child is asking if they can run at this temperature.
#     Rules:
#     - If temperature >= 26°C → allow running
#     - If temperature < 26°C → do not allow running

   
#     """,
#     output_type=RunOutput
# )

# # Guardrail function — input validation & rule enforcement
# @input_guardrail
# async def temperature_input_guard(ctx, agent, input):
#     try:
#         temperature_c = float(input)  # Convert to number
#     except ValueError:
#         return GuardrailFunctionOutput(
#             output_info="Invalid temperature input.",
#             tripwire_triggered=True
#         )

#     # Rule: stop running if temperature < 26°C
#     if temperature_c < 26.0:
#         return GuardrailFunctionOutput(
#             output_info=f"Temperature {temperature_c}°C is below 26°C. You cannot run.",
#             tripwire_triggered=True
#         )

#     # If safe, run father_guard agent
#     result = await Runner.run(father_guard, input, run_config=config)
#     rich.print(result.final_output)

#     return GuardrailFunctionOutput(
#         output_info=result.final_output.response,
#         tripwire_triggered=not result.final_output.canRun
#     )

# # Main Father Agent — asks guardrail before answering
# father_agent = Agent(
#     name="Father Agent",
#     instructions="You are the child's father. Ask me the temperature to decide.",
#     input_guardrails=[temperature_input_guard]
# )

# # Run demo
# async def main():
#     with trace("Father Guardrail Test"):
#         try:
#             # Change this value to test
#             result = await Runner.run(father_agent, "30", run_config=config)
#             print("✅ Request accepted:", result.final_output)

#         except InputGuardrailTripwireTriggered:
#             print("⚠️ You are not allowed to run due to low temperature.")

# if __name__ == "__main__":
#     asyncio.run(main())


#################################################### Exercise 3 #################################################################
# Exercise # 3 Objective: Make a gate keeper agent and gate keeper guardrail. The gate keeper stopping students of other school.


from agents  import (Agent, Runner, trace, input_guardrail, GuardrailFunctionOutput, InputGuardrailTripwireTriggered)
from connection import config
import asyncio
import rich
from pydantic import BaseModel
class enterSchool(BaseModel):
    response: str
    isAllowed: bool
# Gate Keeper Guard agent

gate_keeper_guard=Agent(
    name="Gate Keeper Guard",
    instructions="""
    You are a gate keeper. Only allow students from XYZ School to enter.
    If the student mentions another school, deny entry.
    """,
    output_type=enterSchool
)
# Guardrail function
@input_guardrail
async def school_input_guard(ctx,agent,input):
    allowed_school= "XYZ school"    
    if allowed_school.lower() not in input.lower():
        return GuardrailFunctionOutput(
            output_info=f"❌ Access Denied! Only students from {allowed_school} are allowed.",
            tripwire_triggered=True
        )
     # If allowed, run the decision-making agent
    result = await Runner.run(gate_keeper_guard, input,run_config=config)
    rich.print(result.final_output)
    return GuardrailFunctionOutput(
        output_info=" ✅ Access Granted! Welcome to the school.",
        tripwire_triggered= not result.final_output.isAllowed
    )
# Main Gate Keeper Agent
gate_keeper_agent=Agent(
    name=" Gate Keeper Agent",
    instructions="""You are the school gatekeeper. Ask for the student's school name to decide.
""",
    input_guardrails=[school_input_guard]
)
# Run everything inside main
async def main():
    with trace("Gate Keeper Guardrail"):
        try:
            result=await Runner.run(gate_keeper_agent,"I am from ABC school", run_config=config)
            print(result.final_output)
        except:
             print("❌ Access Denied! Only students from XYZ school are allowed.")

# Run main with asyncio
if __name__ == "__main__":
    asyncio.run(main())
   
