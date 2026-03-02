<script lang="ts">
	import * as InputGroup from '$lib/components/ui/input-group/index.js';
	import { Separator } from '$lib/components/ui/separator/index.js';
	import { handleError } from '$lib/consts.js';
	import { analyzeMovieScript, findMovieScripts } from '$lib/data.remote.js';
	import ArrowUpIcon from '@lucide/svelte/icons/arrow-up';
	import PlusIcon from '@lucide/svelte/icons/plus';
	import { toast } from 'svelte-sonner';

	let btnDisabled = $state(false);
	let query = $state('titanic');
	let options = $state<string[]>([]);

	const suggestions = [
		'titanic',
		'inception',
		'the godfather',
		'interstellar',
		'fight club',
		'parasite'
	];

	async function localFindMovieScripts() {
		btnDisabled = true;
		options = [];
		try {
			options = await findMovieScripts({ query });
		} catch (err) {
			handleError(err);
		}
		btnDisabled = false;
	}

	async function localAnalyzeMovieScripts(scriptUrl: string) {
		btnDisabled = true;
		try {
			const script = await analyzeMovieScript({ scriptUrl });
			console.log(script);
			toast.success('Analysis complete');
		} catch (err) {
			handleError(err);
		}
		btnDisabled = false;
	}
</script>

<div class="mx-auto flex h-full w-full max-w-5xl flex-col items-center justify-center">
	<div class="relative w-full max-w-3xl">
		<div
			class="absolute -inset-px rounded-3xl bg-linear-to-r from-pink-400 via-purple-400 to-blue-400 opacity-80 blur-[2px]"
		></div>

		<div
			class="relative rounded-3xl border border-slate-200/60 bg-white/80 p-8 shadow-xl backdrop-blur"
		>
			<div class="flex items-center gap-3">
				<span
					class="inline-flex items-center rounded-full bg-slate-900 px-3 py-1 text-xs font-medium text-white"
				>
					Digital Think Tank
				</span>
				<span class="text-xs text-slate-500">Script Search + Analysis</span>
			</div>

			<h1 class="mt-4 text-4xl leading-tight font-extrabold text-slate-900">
				Find a movie script, then<br />
				analyze it in seconds.
			</h1>

			<p class="mt-3 max-w-2xl text-sm leading-relaxed text-slate-600">
				Type a movie name to fetch available scripts. Then click any result to run analysis.
			</p>

			<Separator class="my-6" />

			<InputGroup.Root
				class="rounded-2xl border border-slate-200 bg-white focus-within:border-slate-300 focus-within:[box-shadow:0_0_0_4px_rgba(236,72,153,0.12),0_0_0_8px_rgba(59,130,246,0.10)]"
			>
				<textarea
					bind:value={query}
					placeholder="Ask, Search or Chat..."
					rows="2"
					class="w-full resize-none border-none bg-transparent px-4 py-4 text-base text-slate-900 placeholder:text-slate-400 focus:outline-none"
				></textarea>

				<InputGroup.Addon align="block-end">
					<InputGroup.Button
						variant="default"
						class="mr-2 mb-2 ml-auto cursor-pointer rounded-full bg-linear-to-r
            from-pink-500 via-purple-500 to-blue-500 p-3
            text-white shadow-md shadow-pink-500/20 transition hover:opacity-95 active:scale-[0.98]"
						size="icon-xs"
						onclick={localFindMovieScripts}
						disabled={btnDisabled}
					>
						<ArrowUpIcon />
						<span class="sr-only">Search</span>
					</InputGroup.Button>
				</InputGroup.Addon>
			</InputGroup.Root>

			<div class="mt-4 flex flex-wrap gap-2">
				{#each suggestions as s (s)}
					<button
						type="button"
						class="rounded-full border border-slate-200 bg-white px-3 py-1.5 text-xs text-slate-700 transition hover:bg-slate-50"
						disabled={btnDisabled}
						onclick={async () => {
							try {
								btnDisabled = true;
								query = s;
								await localFindMovieScripts();
							} catch (err) {
								handleError(err);
							} finally {
								btnDisabled = false;
							}
						}}
					>
						{s}
					</button>
				{/each}
			</div>

			{#if btnDisabled}
				<div class="mt-4 flex items-center gap-2 text-sm text-slate-600">
					<span class="h-2 w-2 animate-pulse rounded-full bg-pink-500"></span>
					Working...
				</div>
			{/if}

			{#if options.length > 0}
				<Separator class="my-6" />

				<div class="flex items-center justify-between">
					<h2 class="text-sm font-semibold text-slate-900">Results</h2>
					<p class="text-xs text-slate-500">{options.length} found</p>
				</div>

				<div class="mt-4 grid gap-3">
					{#each options as script (script)}
						<button
							type="button"
							disabled={btnDisabled}
							onclick={async () => await localAnalyzeMovieScripts(script)}
							class="group flex w-full items-start justify-between gap-4 rounded-2xl border border-slate-200 bg-white px-4 py-4 text-left transition
                 hover:border-slate-300 hover:bg-slate-50 active:scale-[0.995]"
						>
							<div class="min-w-0">
								<p class="truncate text-sm font-medium text-slate-900">{script}</p>
								<p class="mt-1 text-xs text-slate-500">Click to analyze this script</p>
							</div>

							<span
								class="shrink-0 rounded-full border border-slate-200 bg-white p-2 text-slate-700 transition group-hover:bg-slate-50"
							>
								<PlusIcon class="h-4 w-4" />
							</span>
						</button>
					{/each}
				</div>
			{:else}
				<div class="mt-6 rounded-2xl border border-slate-200 bg-white px-4 py-3">
					<p class="text-sm text-slate-600">
						Tip: search by movie title (e.g., <span class="font-medium text-slate-900">Titanic</span
						>).
					</p>
				</div>
			{/if}
		</div>
	</div>
</div>
