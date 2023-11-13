from typing import Union

DEFAULT_SALE_STAGES = {
    "1": "Introduction: Start the conversation by introducing yourself and your company. Be polite and respectful while keeping the tone of the conversation professional. Your greeting should be welcoming. Always clarify in your greeting the reason why you are calling.",
    "2": "Qualification: Qualify the prospect by confirming if they are the right person to talk to regarding your product/service. Ensure that they have the authority to make purchasing decisions.",
    "3": "Value proposition: Briefly explain how your product/service can benefit the prospect. Focus on the unique selling points and value proposition of your product/service that sets it apart from competitors.",
    "4": "Needs analysis: Ask open-ended questions to uncover the prospect's needs and pain points. Listen carefully to their responses and take notes.",
    "5": "Solution presentation: Based on the prospect's needs, present your product/service as the solution that can address their pain points.",
    "6": "Objection handling: Address any objections that the prospect may have regarding your product/service. Be prepared to provide evidence or testimonials to support your claims.",
    "7": "Close: Ask for the sale by proposing a next step. This could be a demo, a trial or a meeting with decision-makers. Ensure to summarize what has been discussed and reiterate the benefits.",
    "8": "End conversation: It's time to end the call as there is nothing else to be said.",
}

INSURANCE_SALES_STAGES = {
    "1": "**开场白**: 首先，介绍自己和公司，语气要亲切而专业，明确告知打电话的目的",
    "2": "**挖掘需求**: 客户信息收集，包括客户年龄、家庭信息、计划投入金额、购买保险产品的意愿和场景，请注意信息收集的过程不要过于直白",
    "3": "**产品介绍**: 增额寿类保险产品介绍，突出增值、安全稳定、资金灵活、配置灵活和特色权益等特点，请注意不要过于夸大产品优势，保持客观",
    "4": "**配置方案**: 根据客户提供的信息，分析和计算增额售保险产品的现金价值",
    "5": "**销售促成**: 讲解当前最新市场行情、福利政策以及在支付宝上如何进行大额支付",
    "6": "**售后稳单**: 售后服务介绍，包括保单获取和回访，以及转介绍其他保险产品",
}

STAGES_TEMPLATE_MAP = {
    'insurance_broker_prompt': INSURANCE_SALES_STAGES,
    'default': DEFAULT_SALE_STAGES,
}


class StagesManager:
    @staticmethod
    def get_stages_as_string(template_id: str = None) -> str:
        stages = STAGES_TEMPLATE_MAP.get(template_id)
        if stages is None:
            stages = DEFAULT_SALE_STAGES
        return "\n".join(
            [f"{key}: {value}" for key, value in stages.items()]
        )

    @staticmethod
    def get_stage_by_id(stage_id: Union[str, int], template_id: str = None) -> Union[str, None]:
        stages = STAGES_TEMPLATE_MAP.get(template_id)
        if stages is None:
            stages = DEFAULT_SALE_STAGES
        return stages.get(str(stage_id))
