import { explainPattern } from '$lib/server/rag-api';
import { json, error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = async ({ request }) => {
	const { patternName } = await request.json();

	if (!patternName || typeof patternName !== 'string') {
		error(400, 'patternName is required');
	}

	const result = await explainPattern(patternName);
	if (!result) error(503, 'RAG service unavailable');

	return json(result);
};
