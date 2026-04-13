export interface Finding {
	type: 'danger' | 'warning' | 'info';
	title: string;
	description: string;
	matched_pattern: string | null;
}

export interface AnalyzeResponse {
	content: string;
	findings: Finding[];
	patterns_detected: string[];
	confidence_score: number | null;
}

export interface PatternSearchResult {
	content: string;
	metadata: Record<string, unknown>;
	relevance_score: number;
}

export interface PatternSearchResponse {
	query: string;
	results: PatternSearchResult[];
	count: number;
}

export interface PatternExplanation {
	pattern_name: string;
	explanation: string;
	key_red_flags: string[];
	safety_tips: string[];
}

export interface PatternComparison {
	pattern_a: string;
	pattern_b: string;
	similarities: string[];
	differences: string[];
	combined_danger: string;
}

export interface SafetyPlan {
	immediate_steps: string[];
	long_term_strategies: string[];
	resources: string[];
	affirmation: string;
}

export interface Typology {
	name: string;
	summary: string | null;
	main_motivation: string[] | null;
	red_flags: string[] | null;
	[key: string]: unknown;
}

export interface PatternComparison {
	pattern_a: string;
	pattern_b: string;
	similarities: string[];
	differences: string[];
	combined_danger: string;
}

export interface SafetyPlan {
	immediate_steps: string[];
	long_term_strategies: string[];
	resources: string[];
	affirmation: string;
}

export interface SearchResponse {
	query: string;
	results: { content: string; metadata: Record<string, unknown>; relevance_score: number }[];
	count: number;
}
