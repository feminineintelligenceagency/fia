import { command, getRequestEvent } from '$app/server';
import { fromAbsolute } from '@internationalized/date';
import { ChatOpenAI } from '@langchain/openai';
import { error } from '@sveltejs/kit';
import { type } from 'arktype';
import { JSDOM } from 'jsdom';
import { createAgent } from 'langchain';
import { API_KEY_COOKIE, getTimestampInSeconds } from './consts';
import { mainAgentPrompt, postAnalystSubagentPrompt } from './server/prompts';
import {
	callPostAnalystSubagent,
	getAllPlayerTypologies,
	getPlayerTypologyInformationByName,
	savePostToDB
} from './server/tools';

export const findMovieScripts = command(type({ query: 'string > 0' }), async ({ query }) => {
	const fd = new FormData();

	fd.set('search_query', query);
	fd.set('submit', 'Go!');

	const req = await fetch('https://imsdb.com/search.php', {
		method: 'POST',
		body: fd
	});

	let htmlString = await req.text();

	htmlString = htmlString.substring(
		htmlString.indexOf('<br><h1>Search results for '),
		htmlString.indexOf('<script type="text/javascript" src="/a/a_imsdb_rec_goo.js"></script>')
	);

	const dom = new JSDOM(htmlString);

	const anchorTags = dom.window.document.querySelectorAll('a');

	const hrefs: string[] = Array.from(anchorTags).map((anchor) => anchor.href);

	if (hrefs.length === 0) {
		error(500, "couldn't file the movie script");
	}

	const options = hrefs.map(
		(h) =>
			`https://imsdb.com/scripts/${h.replace('/Movie Scripts/', '').replace('/TV Transcripts/', '').replace(' Script.html', '').replaceAll(' - ', '-').replaceAll(' ', '-')}.html`
	);

	return options;
});

function chunkText(text: string, chunkSize: number = 4096) {
	const result = [];
	for (let i = 0; i < text.length; i += chunkSize) {
		result.push(text.slice(i, i + chunkSize));
	}
	return result;
}

export const analyzeMovieScript = command(
	type({ scriptUrl: 'string.url' }),
	async ({ scriptUrl }) => {
		const { cookies } = getRequestEvent();

		const apiKey = cookies.get(API_KEY_COOKIE);

		if (!apiKey) {
			error(500, 'No api key set');
		}

		const llm = new ChatOpenAI({
			model: 'gpt-5-nano',
			maxRetries: 2,
			apiKey
		});

		const postAnalystSubagent = createAgent({
			model: llm,
			tools: [savePostToDB, getAllPlayerTypologies, getPlayerTypologyInformationByName],
			systemPrompt: postAnalystSubagentPrompt
		});

		const agent = createAgent({
			model: llm,
			tools: [callPostAnalystSubagent(postAnalystSubagent)],
			systemPrompt: mainAgentPrompt
		});

		const req = await fetch(scriptUrl, {});

		let htmlString = await req.text();

		const strToFind = '<td class="scrtext">';

		htmlString = htmlString.substring(
			htmlString.indexOf(strToFind) + strToFind.length,
			htmlString.indexOf('<table width="85%" border="0"')
		);

		const chunks = chunkText(htmlString);
		let k = 0;
		for (const chunk of chunks) {
			await agent.invoke({
				messages: [{ role: 'human', content: chunk }]
			});
			k++;

			if (k > 9) {
				break;
			}
		}

		return 'done';
	}
);

export const setApiKey = command(type('string > 0'), async (key) => {
	const { cookies } = getRequestEvent();

	if (!key.startsWith('sk-')) {
		error(500, 'Wrong api key format');
	}

	const maxAge = getTimestampInSeconds() + 90 * 24 * 60 * 60; // 90 days in seconds

	const date = fromAbsolute(maxAge * 1000, 'America/Phoenix').toDate();

	cookies.set(API_KEY_COOKIE, key, {
		path: '/',
		httpOnly: true,
		secure: true,
		maxAge,
		expires: date
	});
});
