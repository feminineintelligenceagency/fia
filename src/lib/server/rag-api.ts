import { env } from '$env/dynamic/private';
import type {
	AnalyzeResponse,
	PatternExplanation,
	PatternComparison,
	SafetyPlan,
	Typology
} from '$lib/types/rag';

function getBaseUrl(): string {
	return env.RAG_API_URL ?? 'http://localhost:8000';
}

async function ragFetch<T>(path: string, options?: RequestInit): Promise<T | null> {
	try {
		const res = await fetch(`${getBaseUrl()}${path}`, {
			...options,
			headers: {
				'Content-Type': 'application/json',
				...options?.headers
			}
		});

		if (!res.ok) return null;
		return (await res.json()) as T;
	} catch {
		return null;
	}
}

export async function analyzeContent(content: string): Promise<AnalyzeResponse | null> {
	return ragFetch<AnalyzeResponse>('/analyze', {
		method: 'POST',
		body: JSON.stringify({ content })
	});
}

export async function searchRAG(
	query: string,
	k: number = 5,
	category?: string
): Promise<{ query: string; results: unknown[]; count: number } | null> {
	const params = new URLSearchParams({ query, k: String(k) });
	if (category) params.set('category', category);

	return ragFetch(`/search?${params}`, { method: 'POST' });
}

export async function getTypologies(): Promise<Typology[] | null> {
	return ragFetch<Typology[]>('/typologies');
}

export async function getAbuseFlavors(): Promise<Record<string, unknown>[] | null> {
	return ragFetch<Record<string, unknown>[]>('/abuse-flavors');
}

export async function explainPattern(patternName: string): Promise<PatternExplanation | null> {
	return ragFetch<PatternExplanation>('/explain-pattern', {
		method: 'POST',
		body: JSON.stringify({ pattern_name: patternName })
	});
}

export async function comparePatterns(
	patternA: string,
	patternB: string
): Promise<PatternComparison | null> {
	return ragFetch<PatternComparison>('/compare-patterns', {
		method: 'POST',
		body: JSON.stringify({ pattern_a: patternA, pattern_b: patternB })
	});
}

export async function generateSafetyPlan(
	story: string,
	patternsDetected: string[]
): Promise<SafetyPlan | null> {
	return ragFetch<SafetyPlan>('/safety-plan', {
		method: 'POST',
		body: JSON.stringify({ story, patterns_detected: patternsDetected })
	});
}
