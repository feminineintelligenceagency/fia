import { generateSafetyPlan } from '$lib/server/rag-api';
import { json, error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = async ({ request }) => {
	const { story, patternsDetected } = await request.json();

	if (!story || typeof story !== 'string') {
		error(400, 'story is required');
	}
	if (!Array.isArray(patternsDetected)) {
		error(400, 'patternsDetected must be an array');
	}

	const result = await generateSafetyPlan(story, patternsDetected);
	if (!result) error(503, 'RAG service unavailable');

	return json(result);
};
