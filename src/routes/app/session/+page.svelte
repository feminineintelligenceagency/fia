<script lang="ts">
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';

	import { Separator } from '$lib/components/ui/separator/index.js';
	import { Button } from '$lib/components/ui/button/index.js';

	import {
		privateMode,
		sessionResults,
		activeResultId,
		setActiveResult,
		clearSession,
		stopPrivateMode
	} from '$lib/stores/privatemode';

	const active = $derived.by(() => {
		const list = $sessionResults;
		const id = $activeResultId;
		return list.find((x) => x.id === id) ?? list[0];
	});

	$effect(() => {
		if (active && $activeResultId !== active.id) setActiveResult(active.id);
	});

	function closeSession() {
		clearSession();
		stopPrivateMode();
		goto(resolve('/app'));
	}

	function resultBtnClass(id: string) {
		const isActive = active?.id === id;

		return (
			'w-full rounded-xl border px-3 py-3 text-left transition ' +
			'border-slate-200 bg-white text-slate-900 hover:bg-slate-50 ' +
			'dark:border-slate-700/40 dark:bg-slate-950/30 dark:text-slate-100 dark:hover:bg-slate-900/40 ' +
			(isActive ? ' ring-2 ring-pink-400/50 border-pink-300/60 dark:border-pink-400/40' : '')
		);
	}
</script>

<div class="min-h-screen w-full bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-100">
	<div class="mx-auto flex w-full max-w-6xl flex-col gap-4 p-4">
		<div class="flex items-center justify-between">
			<div>
				<h1 class="text-2xl font-extrabold text-slate-900 dark:text-slate-100">Session Results</h1>
				<p class="text-sm text-slate-600 dark:text-slate-300">
					{#if $privateMode}
						Private Mode is ON — nothing here is saved.
					{:else}
						Private Mode is OFF.
					{/if}
				</p>
			</div>

			<div class="flex items-center gap-2">
				<Button
					variant="outline"
					class="border-slate-300 bg-white text-slate-800 hover:bg-slate-50
					       dark:border-slate-700/50 dark:bg-slate-900/40 dark:text-slate-100 dark:hover:bg-slate-900/60"
					onclick={() => goto(resolve('/app'))}
				>
					Back
				</Button>

				<Button class="bg-pink-500 text-white hover:opacity-95" onclick={closeSession}>
					Close Session
				</Button>
			</div>
		</div>

		<Separator class="border-slate-200 dark:border-slate-700/40" />

		{#if $sessionResults.length === 0}
			<div
				class="rounded-2xl border border-slate-200 bg-white/80 p-6 text-slate-700 shadow-sm
				       dark:border-slate-700/40 dark:bg-slate-950/30 dark:text-slate-200"
			>
				No results yet. Run an analysis and it will appear here.
			</div>
		{:else}
			<div class="grid grid-cols-1 gap-4 md:grid-cols-3">
				<div
					class="rounded-2xl border border-slate-200 bg-white/80 p-4 shadow-sm
					       dark:border-slate-700/40 dark:bg-slate-950/30"
				>
					<p class="mb-3 text-xs font-semibold tracking-widest text-slate-500 dark:text-slate-300">
						RESULTS
					</p>

					<div class="flex flex-col gap-2">
						{#each $sessionResults as r (r.id)}
							<button type="button" onclick={() => setActiveResult(r.id)} class={resultBtnClass(r.id)}>
								<p class="truncate text-sm font-semibold">{r.title}</p>
								<p class="truncate text-xs text-slate-500 dark:text-slate-300">
									{new Date(r.createdAt).toLocaleString()}
								</p>
							</button>
						{/each}
					</div>
				</div>

				<div
					class="md:col-span-2 rounded-2xl border border-slate-200 bg-white/80 p-4 shadow-sm
					       dark:border-slate-700/40 dark:bg-slate-950/30"
				>
					<p class="mb-2 text-xs font-semibold tracking-widest text-slate-500 dark:text-slate-300">
						DETAILS
					</p>

					{#if active}
						<h2 class="text-lg font-bold text-slate-900 dark:text-slate-100">{active.title}</h2>
						<p class="mt-1 break-all text-xs text-slate-600 dark:text-slate-300">{active.source}</p>

						<Separator class="my-4 border-slate-200 dark:border-slate-700/40" />

						<pre
							class="max-h-[60vh] overflow-auto rounded-xl bg-slate-900 p-4 text-xs text-slate-100
							       dark:bg-black/40"
						>{JSON.stringify(active.result ?? null, null, 2) || 'No result payload'}</pre>
					{/if}
				</div>
			</div>
		{/if}
	</div>
</div>