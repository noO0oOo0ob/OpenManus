import os
from pathlib import Path

# 确保uml目录存在
os.makedirs("uml", exist_ok=True)

# 类图
class_diagram = """
@startuml OpenManus_Class_Diagram

' 样式设置
skinparam classAttributeIconSize 0
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName "Arial"
skinparam packageStyle rectangle

' 基础代理类
abstract class BaseAgent {
    +name: str
    +description: Optional[str]
    +system_prompt: Optional[str]
    +next_step_prompt: Optional[str]
    +llm: LLM
    +memory: Memory
    +state: AgentState
    +max_steps: int
    +current_step: int
    +run(request: str): str
    +{abstract} step(): str
}

' ReAct代理类
abstract class ReActAgent {
    +name: str
    +description: Optional[str]
    +system_prompt: Optional[str]
    +next_step_prompt: Optional[str]
    +llm: LLM
    +memory: Memory
    +state: AgentState
    +max_steps: int
    +current_step: int
    +{abstract} think(): bool
    +{abstract} act(): str
    +step(): str
}

' 工具调用代理类
class ToolCallAgent {
    +name: str
    +description: str
    +system_prompt: str
    +next_step_prompt: str
    +available_tools: ToolCollection
    +tool_choices: Literal
    +special_tool_names: List[str]
    +tool_calls: List[ToolCall]
    +max_steps: int
    +think(): bool
    +act(): str
    +execute_tool(tool_call: ToolCall): Any
}

' Manus代理类
class Manus {
    +name: str
    +description: str
    +system_prompt: str
    +next_step_prompt: str
    +available_tools: ToolCollection
    +max_steps: int
}

' 基础流程类
abstract class BaseFlow {
    +agents: Dict[str, BaseAgent]
    +tools: Optional[List]
    +primary_agent_key: Optional[str]
    +primary_agent: Optional[BaseAgent]
    +get_agent(key: str): Optional[BaseAgent]
    +add_agent(key: str, agent: BaseAgent): None
    +{abstract} execute(input_text: str): str
}

' 规划流程类
class PlanningFlow {
    +llm: LLM
    +planning_tool: PlanningTool
    +executor_keys: List[str]
    +active_plan_id: str
    +current_step_index: Optional[int]
    +get_executor(step_type: Optional[str]): BaseAgent
    +execute(input_text: str): str
    -_create_initial_plan(input_text: str): Dict
    -_execute_step(step: Dict, executor: BaseAgent): str
    -_mark_step_completed(step_index: int): None
    -_finalize_plan(): str
}

' 流程工厂类
class FlowFactory {
    +{static} create_flow(flow_type: FlowType, agents: Union[BaseAgent, List[BaseAgent], Dict[str, BaseAgent]], **kwargs): BaseFlow
}

' 枚举类型
enum FlowType {
    PLANNING
}

enum AgentState {
    IDLE
    RUNNING
    COMPLETED
    ERROR
}

enum PlanStepStatus {
    NOT_STARTED
    IN_PROGRESS
    COMPLETED
    BLOCKED
}

' 工具相关类
class ToolCollection {
    +tools: List[BaseTool]
    +add(tool: BaseTool): None
    +get(name: str): Optional[BaseTool]
    +to_params(): List[Dict]
}

abstract class BaseTool {
    +name: str
    +description: str
    +parameters: Dict
    +{abstract} _run(**kwargs): Any
}

class PlanningTool {
    +name: str
    +description: str
    +parameters: Dict
    +_run(**kwargs): Any
}

' 其他相关类
class LLM {
    +ask(messages: List[Message], system_msgs: Optional[List[Message]]): Message
    +ask_tool(messages: List[Message], system_msgs: Optional[List[Message]], tools: List[Dict], tool_choice: str): Message
}

class Memory {
    +messages: List[Message]
    +add_message(message: Message): None
    +get_messages(): List[Message]
    +clear(): None
}

class Message {
    +role: str
    +content: str
    +{static} system_message(content: str): Message
    +{static} user_message(content: str): Message
    +{static} assistant_message(content: str): Message
}

' 关系定义
BaseAgent <|-- ReActAgent
ReActAgent <|-- ToolCallAgent
ToolCallAgent <|-- Manus

BaseFlow <|-- PlanningFlow

BaseAgent --> AgentState
BaseAgent --> Memory
BaseAgent --> LLM

BaseFlow --> BaseAgent

PlanningFlow --> PlanningTool
PlanningFlow --> LLM
PlanningFlow --> PlanStepStatus

FlowFactory --> FlowType
FlowFactory --> BaseFlow
FlowFactory --> PlanningFlow

ToolCallAgent --> ToolCollection
ToolCollection --> BaseTool
BaseTool <|-- PlanningTool

Memory --> Message

@enduml
"""

# 序列图
sequence_diagram = """
@startuml OpenManus_Sequence_Diagram

' 样式设置
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName "Arial"
skinparam sequenceMessageAlign center

actor User
participant "run_flow.py" as RunFlow
participant "FlowFactory" as Factory
participant "PlanningFlow" as Flow
participant "Manus" as Agent
participant "ToolCallAgent" as ToolAgent
participant "LLM" as LLM
participant "Tools" as Tools

User -> RunFlow: 输入提示词
activate RunFlow

RunFlow -> Factory: create_flow(FlowType.PLANNING, agents)
activate Factory
Factory --> RunFlow: 返回 PlanningFlow 实例
deactivate Factory

RunFlow -> Flow: execute(prompt)
activate Flow

Flow -> Flow: _create_initial_plan(prompt)
activate Flow #DarkGray
Flow -> LLM: 请求生成初始计划
activate LLM
LLM --> Flow: 返回初始计划
deactivate LLM
deactivate Flow

loop 对每个计划步骤
    Flow -> Flow: _get_current_step_info()
    Flow -> Flow: get_executor()
    Flow -> Agent: run(step_request)
    activate Agent
    
    Agent -> ToolAgent: think()
    activate ToolAgent
    ToolAgent -> LLM: ask_tool(messages, tools)
    activate LLM
    LLM --> ToolAgent: 返回工具调用
    deactivate LLM
    ToolAgent --> Agent: 返回工具调用结果
    deactivate ToolAgent
    
    Agent -> ToolAgent: act()
    activate ToolAgent
    ToolAgent -> Tools: execute_tool(tool_call)
    activate Tools
    Tools --> ToolAgent: 返回工具执行结果
    deactivate Tools
    ToolAgent --> Agent: 返回执行结果
    deactivate ToolAgent
    
    Agent --> Flow: 返回步骤执行结果
    deactivate Agent
    
    Flow -> Flow: _mark_step_completed(step_index)
end

Flow -> Flow: _finalize_plan()
Flow --> RunFlow: 返回执行结果
deactivate Flow

RunFlow --> User: 显示执行结果
deactivate RunFlow

@enduml
"""

# 组件图
component_diagram = """
@startuml OpenManus_Component_Diagram

' 样式设置
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName "Arial"
skinparam componentStyle uml2

package "入口点" {
    [run_flow.py] as RunFlow
}

package "代理系统" {
    [BaseAgent] as BaseAgent
    [ReActAgent] as ReActAgent
    [ToolCallAgent] as ToolAgent
    [Manus] as Manus
}

package "流程管理" {
    [BaseFlow] as BaseFlow
    [PlanningFlow] as PlanningFlow
    [FlowFactory] as FlowFactory
}

package "工具系统" {
    [ToolCollection] as ToolCollection
    [BaseTool] as BaseTool
    [PlanningTool] as PlanningTool
    [PythonExecute] as PythonExecute
    [GoogleSearch] as GoogleSearch
    [BrowserUseTool] as BrowserUseTool
    [FileSaver] as FileSaver
    [Terminate] as Terminate
}

package "核心服务" {
    [LLM] as LLM
    [Memory] as Memory
    [Message] as Message
    [AgentState] as AgentState
    [PlanStepStatus] as PlanStepStatus
}

' 关系定义
RunFlow --> FlowFactory: 创建流程
RunFlow --> Manus: 创建代理

FlowFactory --> PlanningFlow: 创建实例
PlanningFlow --> BaseFlow: 继承
PlanningFlow --> LLM: 使用
PlanningFlow --> PlanningTool: 使用
PlanningFlow --> Manus: 调用

Manus --> ToolAgent: 继承
ToolAgent --> ReActAgent: 继承
ReActAgent --> BaseAgent: 继承

BaseAgent --> Memory: 使用
BaseAgent --> LLM: 使用
BaseAgent --> AgentState: 使用

ToolAgent --> ToolCollection: 使用
ToolCollection --> BaseTool: 包含
BaseTool <|-- PlanningTool
BaseTool <|-- PythonExecute
BaseTool <|-- GoogleSearch
BaseTool <|-- BrowserUseTool
BaseTool <|-- FileSaver
BaseTool <|-- Terminate

Memory --> Message: 包含

@enduml
"""

# 活动图
activity_diagram = """
@startuml OpenManus_Activity_Diagram

' 样式设置
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName "Arial"
skinparam activityDiamondBackgroundColor white

start

:用户输入提示词;

:创建 Manus 代理实例;

:通过 FlowFactory 创建 PlanningFlow 实例;

:PlanningFlow 创建初始计划;

while (还有未完成的步骤?) is (是)
  :获取当前步骤信息;
  
  :获取执行器代理;
  
  :执行步骤;
  
  fork
    :代理思考 (think);
    :使用 LLM 生成工具调用;
  fork again
    :代理行动 (act);
    :执行工具调用;
  end fork
  
  :标记步骤完成;
endwhile (否)

:完成计划;

:返回执行结果给用户;

stop

@enduml
"""

# 部署图
deployment_diagram = """
@startuml OpenManus_Deployment_Diagram

' 样式设置
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName "Arial"

node "用户环境" {
    [命令行界面] as CLI
    [Python 运行时] as PythonRuntime
}

node "OpenManus 系统" {
    package "核心组件" {
        [run_flow.py] as RunFlow
        [代理系统] as AgentSystem
        [流程管理] as FlowSystem
        [工具系统] as ToolSystem
    }
    
    database "内存存储" {
        [代理状态] as AgentState
        [消息历史] as MessageHistory
        [计划数据] as PlanData
    }
}

cloud "外部服务" {
    [LLM API] as LLMAPI
    [搜索服务] as SearchService
    [浏览器服务] as BrowserService
}

CLI --> RunFlow : 用户输入
RunFlow --> AgentSystem : 创建代理
RunFlow --> FlowSystem : 创建流程
AgentSystem --> ToolSystem : 使用工具
FlowSystem --> AgentSystem : 调用代理

AgentSystem --> AgentState : 存储状态
AgentSystem --> MessageHistory : 存储消息
FlowSystem --> PlanData : 存储计划

ToolSystem --> LLMAPI : API调用
ToolSystem --> SearchService : 搜索请求
ToolSystem --> BrowserService : 浏览器操作

RunFlow --> CLI : 返回结果

@enduml
"""

# 写入文件
with open("uml/class_diagram.puml", "w") as f:
    f.write(class_diagram)

with open("uml/sequence_diagram.puml", "w") as f:
    f.write(sequence_diagram)

with open("uml/component_diagram.puml", "w") as f:
    f.write(component_diagram)

with open("uml/activity_diagram.puml", "w") as f:
    f.write(activity_diagram)

with open("uml/deployment_diagram.puml", "w") as f:
    f.write(deployment_diagram)

print("UML 图文件已生成到 uml/ 目录") 