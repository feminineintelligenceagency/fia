import { comparePatterns } from '$lib/server/rag-api';
import { json, error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = async ({ request }) => {
	const { patternA, patternB } = await request.json();

	if (!patternA || typeof patternA !== 'string') {
		error(400, 'patternA is required');
	}
	if (!patternB || typeof patternB !== 'string') {
		error(400, 'patternB is required');
	}

	const result = await comparePatterns(patternA, patternB);
	if (!result) error(503, 'RAG service unavailable');

	return json(result);
};
