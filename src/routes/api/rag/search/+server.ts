import { searchRAG } from '$lib/server/rag-api';
import { json, error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = async ({ request }) => {
	const { query, k = 5 } = await request.json();

	if (!query || typeof query !== 'string') {
		error(400, 'query is required');
	}

	const result = await searchRAG(query, k);
	if (!result) error(503, 'RAG service unavailable');

	return json(result);
};
