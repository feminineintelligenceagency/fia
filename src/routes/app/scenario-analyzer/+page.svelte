<script lang="ts">
	import { Button } from '$lib/components/ui/button/index.js';
	import { Textarea } from '$lib/components/ui/textarea/index.js';
	import { handleError } from '$lib/consts';
	import { analyzeScenario } from '$lib/data.remote';
	import Markdown from 'svelte-exmarkdown';

	let scenario = $state('my girlfriend beats me up');

	let btnDisabled = $state(false);

	let analysis = $state('');
</script>

<div class="flex h-full flex-col">
	<div class="flex-1 overflow-y-auto p-6">
		<article class="mx-auto prose max-w-5xl">
			{#if analysis}
				<Markdown md={analysis} />
			{:else if btnDisabled}
				<p>Analyzing...</p>
			{:else}
				<p>Ask a question to get started.</p>
			{/if}
		</article>
	</div>

	<div class="sticky bottom-0 border-t bg-white/80 p-4 backdrop-blur-md">
		<div class="flex gap-2">
			<Textarea
				bind:value={scenario}
				placeholder="Describe a scenario..."
				disabled={btnDisabled}
				class="max-h-75 flex-1 rounded-xl px-4 py-2"
			/>
			<Button
				onclick={async () => {
					try {
						btnDisabled = true;
						analysis = await analyzeScenario({ scenario });
					} catch (err) {
						handleError(err);
					} finally {
						btnDisabled = false;
					}
				}}
				class="mt-auto bg-pink-500 hover:bg-pink-500/90"
				size="sm"
				disabled={btnDisabled || scenario.trim().length === 0}>Ask</Button
			>
		</div>
	</div>
</div>
