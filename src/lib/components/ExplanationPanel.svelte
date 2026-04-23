<script lang="ts">
	import ChevronLeft from '@lucide/svelte/icons/chevron-left';
	import ChevronRight from '@lucide/svelte/icons/chevron-right';
	import Search from '@lucide/svelte/icons/search';
	import X from '@lucide/svelte/icons/x';

	interface Player {
		id: number;
		name: string;
		summary: string;
		main_motivation: string;
		red_flags: string;
		techniques_he_might_use: string;
	}

	interface Flavor {
		id: number;
		name: string;
	}

	interface Trauma {
		id: number;
		name: string;
		abuse_techniques: string;
		research_summary: string;
	}

	interface Vulnerabilitiy {
		id: number;
		name: string;
		traits: string;
		abuse_techniques: string;
		brain_biases: string;
	}

	let {
		players,
		flavors,
		playerToFlavors,
		playerToTraumas,
		traumas,
		vulnerabilities,
		playerToVulnerabilities
	}: {
		players: Player[];
		flavors: Flavor[];
		playerToFlavors: { player_id: number; flavor_id: number }[];
		playerToTraumas: { player_id: number; trauma_id: number }[];
		traumas: Trauma[];
		vulnerabilities: Vulnerabilitiy[];
		playerToVulnerabilities: { player_id: number; vulnerability_id: number }[];
	} = $props();

	let isOpen = $state(false);
	let activeTab = $state<'typologies' | 'flavors' | 'vulnerabilities' | 'trauma'>('typologies');
	let search = $state('');
</script>

<div class="fixed top-1/2 right-0 z-50 -translate-y-1/2">
	<button
		type="button"
		class="group flex items-center gap-2 rounded-l-2xl border border-slate-200 bg-white/95 px-3 py-3 text-slate-700 shadow-lg transition hover:bg-slate-50"
		onclick={() => (isOpen = !isOpen)}
	>
		{#if isOpen}
			<ChevronRight class="h-5 w-5" />
		{:else}
			<ChevronLeft class="h-5 w-5" />
		{/if}
		<span class="hidden text-xs font-semibold sm:block">Traits Panel</span>
	</button>
</div>

{#if isOpen}
	<button
		type="button"
		class="fixed inset-0 z-40 bg-slate-900/20"
		onclick={() => (isOpen = false)}
		aria-label="Close panel overlay"
	></button>
{/if}

<div
	class={`fixed top-0 right-0 z-50 h-screen w-full max-w-md border-l border-slate-200 bg-white/95 shadow-2xl transition-transform duration-300 ease-in-out sm:max-w-xl ${
		isOpen ? 'translate-x-0' : 'translate-x-full'
	}`}
>
	{#if isOpen}
		<div class="flex h-full flex-col">
			<div class="border-b border-slate-200 px-4 py-4 sm:px-5">
				<div class="flex items-center justify-between gap-3">
					<div>
						<h2 class="text-lg font-bold text-slate-900">Trait Explanation Panel</h2>
						<p class="mt-1 text-xs text-slate-500">
							Browse typologies, abuse flavors, vulnerability types, and trauma signs.
						</p>
					</div>

					<button
						type="button"
						class="rounded-full border border-slate-200 bg-white p-2 text-slate-600 transition hover:bg-slate-50"
						onclick={() => (isOpen = false)}
					>
						<X class="h-4 w-4" />
					</button>
				</div>

				<div class="relative mt-4">
					<Search
						class="pointer-events-none absolute top-1/2 left-3 h-4 w-4 -translate-y-1/2 text-slate-400"
					/>
					<input
						bind:value={search}
						type="text"
						placeholder="Search categories, traits, red flags, techniques..."
						class="w-full rounded-2xl border border-slate-200 bg-white py-3 pr-4 pl-10 text-sm text-slate-800 transition outline-none focus:border-slate-300"
					/>
				</div>

				<div class="mt-4 flex flex-wrap gap-2">
					<button
						type="button"
						class={`rounded-full px-3 py-1.5 text-xs font-semibold transition ${
							activeTab === 'typologies'
								? 'bg-slate-900 text-white'
								: 'bg-slate-100 text-slate-700 hover:bg-slate-200'
						}`}
						onclick={() => (activeTab = 'typologies')}
					>
						Typologies
					</button>

					<button
						type="button"
						class={`rounded-full px-3 py-1.5 text-xs font-semibold transition ${
							activeTab === 'flavors'
								? 'bg-slate-900 text-white'
								: 'bg-slate-100 text-slate-700 hover:bg-slate-200'
						}`}
						onclick={() => (activeTab = 'flavors')}
					>
						Flavors
					</button>

					<button
						type="button"
						class={`rounded-full px-3 py-1.5 text-xs font-semibold transition ${
							activeTab === 'vulnerabilities'
								? 'bg-slate-900 text-white'
								: 'bg-slate-100 text-slate-700 hover:bg-slate-200'
						}`}
						onclick={() => (activeTab = 'vulnerabilities')}
					>
						Vulnerability
					</button>

					<button
						type="button"
						class={`rounded-full px-3 py-1.5 text-xs font-semibold transition ${
							activeTab === 'trauma'
								? 'bg-slate-900 text-white'
								: 'bg-slate-100 text-slate-700 hover:bg-slate-200'
						}`}
						onclick={() => (activeTab = 'trauma')}
					>
						Trauma
					</button>
				</div>
			</div>

			<div class="flex-1 overflow-y-auto px-4 py-4 sm:px-5">
				{#if activeTab === 'typologies'}
					<div class="space-y-3">
						{#each players.filter((_) => _.name
								.toLowerCase()
								.includes(search.toLowerCase())) as player (player.id)}
							{@const ptofls = playerToFlavors
								.filter((_) => _.player_id === player.id)
								.map((_) => _.flavor_id)}
							{@const fls = flavors.filter((_) => ptofls.includes(_.id))}
							<details class="rounded-2xl border border-slate-200 bg-white p-4">
								<summary class="cursor-pointer list-none">
									<h3 class="text-sm font-semibold text-slate-900">{player.name}</h3>
									{#if player.summary}
										<p class="mt-2 line-clamp-3 text-xs leading-5 text-slate-600">
											{player.summary}
										</p>
									{/if}
								</summary>

								<div class="mt-4 space-y-4 border-t border-slate-100 pt-4">
									<div>
										<p
											class="mb-2 text-[11px] font-semibold tracking-wide text-slate-500 uppercase"
										>
											Main motivation
										</p>
										<div class="flex flex-wrap gap-2">
											{#each player.main_motivation.split('\n') as value, n (n)}
												<span
													class="rounded-full bg-slate-100 px-2.5 py-1 text-[11px] text-slate-700"
												>
													{value}
												</span>
											{/each}
										</div>
									</div>

									<div>
										<p
											class="mb-2 text-[11px] font-semibold tracking-wide text-slate-500 uppercase"
										>
											Abuse flavors
										</p>
										<div class="flex flex-wrap gap-2">
											{#each fls as fl (fl.id)}
												<span
													class="rounded-full bg-slate-50 px-2.5 py-1 text-[11px] text-slate-700"
												>
													{fl.name}
												</span>
											{/each}
										</div>
									</div>

									<div>
										<p
											class="mb-2 text-[11px] font-semibold tracking-wide text-slate-500 uppercase"
										>
											Red flags
										</p>
										<ul class="space-y-1 text-xs leading-5 text-slate-600">
											{#each player.red_flags.split('\n') as value, n (n)}
												<li>• {value}</li>
											{/each}
										</ul>
									</div>

									<div>
										<p
											class="mb-2 text-[11px] font-semibold tracking-wide text-slate-500 uppercase"
										>
											Techniques
										</p>
										<ul class="space-y-1 text-xs leading-5 text-slate-600">
											{#each player.techniques_he_might_use.split('\n') as value, n (n)}
												<li>• {value}</li>
											{/each}
										</ul>
									</div>
								</div>
							</details>
						{/each}

						<!-- {#if filteredTypologies.length === 0}
							<p class="text-sm text-slate-500">No typologies matched your search.</p>
						{/if} -->
					</div>
				{/if}

				{#if activeTab === 'flavors'}
					<div class="space-y-3">
						{#each flavors.filter((_) => _.name
								.toLowerCase()
								.includes(search.toLowerCase())) as flavor (flavor.id)}
							{@const ptofls = playerToFlavors
								.filter((_) => _.flavor_id === flavor.id)
								.map((_) => _.player_id)}
							{@const pls = players.filter((_) => ptofls.includes(_.id))}
							<div class="rounded-2xl border border-slate-200 bg-white p-4">
								<h3 class="text-sm font-semibold text-slate-900">{flavor.name}</h3>
								<div class="mt-3 flex flex-wrap gap-2">
									{#each pls as pl (pl.id)}
										<span class="rounded-full bg-slate-100 px-2.5 py-1 text-[11px] text-slate-700">
											{pl.name}
										</span>
									{/each}
								</div>
							</div>
						{/each}
					</div>
				{/if}

				{#if activeTab === 'vulnerabilities'}
					<div class="space-y-3">
						{#each vulnerabilities.filter((_) => _.name
								.toLowerCase()
								.includes(search.toLowerCase())) as vulnerability (vulnerability.id)}
							{@const ptovs = playerToVulnerabilities
								.filter((_) => _.vulnerability_id === vulnerability.id)
								.map((_) => _.player_id)}
							{@const pls = players.filter((_) => ptovs.includes(_.id))}
							<details class="rounded-2xl border border-slate-200 bg-white p-4">
								<summary class="cursor-pointer list-none">
									<h3 class="text-sm font-semibold text-slate-900">{vulnerability.name}</h3>
								</summary>

								<div class="mt-4 space-y-4 border-t border-slate-100 pt-4">
									<div>
										<p
											class="mb-2 text-[11px] font-semibold tracking-wide text-slate-500 uppercase"
										>
											Vulnerability traits
										</p>
										<div class="flex flex-wrap gap-2">
											{#each vulnerability.traits.split('\n') as value, n (n)}
												<span
													class="rounded-full bg-slate-100 px-2.5 py-1 text-[11px] text-slate-700"
												>
													{value}
												</span>
											{/each}
										</div>
									</div>

									<div>
										<p
											class="mb-2 text-[11px] font-semibold tracking-wide text-slate-500 uppercase"
										>
											Abuse techniques
										</p>
										<ul class="space-y-1 text-xs leading-5 text-slate-600">
											{#each vulnerability.abuse_techniques.split('\n') as value, n (n)}
												<li>• {value}</li>
											{/each}
										</ul>
									</div>

									<div>
										<p
											class="mb-2 text-[11px] font-semibold tracking-wide text-slate-500 uppercase"
										>
											Brain biases
										</p>
										<div class="flex flex-wrap gap-2">
											{#each vulnerability.brain_biases.split('\n') as value, n (n)}
												<span
													class="rounded-full bg-slate-50 px-2.5 py-1 text-[11px] text-slate-700"
												>
													{value}
												</span>
											{/each}
										</div>
									</div>

									<div>
										<p
											class="mb-2 text-[11px] font-semibold tracking-wide text-slate-500 uppercase"
										>
											Related typologies
										</p>
										<div class="flex flex-wrap gap-2">
											{#each pls as pl (pl.id)}
												<span
													class="rounded-full bg-slate-50 px-2.5 py-1 text-[11px] text-slate-700"
												>
													{pl.name}
												</span>
											{/each}
										</div>
									</div>
								</div>
							</details>
						{/each}
					</div>
				{/if}

				{#if activeTab === 'trauma'}
					<div class="space-y-3">
						{#each traumas.filter((_) => _.name
								.toLowerCase()
								.includes(search.toLowerCase())) as trauma (trauma.id)}
							{@const ptots = playerToTraumas
								.filter((_) => _.trauma_id === trauma.id)
								.map((_) => _.player_id)}
							{@const pls = players.filter((_) => ptots.includes(_.id))}
							<div class="rounded-2xl border border-slate-200 bg-white p-4">
								<h3 class="text-sm font-semibold text-slate-900">{trauma.name}</h3>

								{#if trauma.research_summary}
									<p class="mt-2 text-xs leading-5 text-slate-600">{trauma.research_summary}</p>
								{/if}

								<div class="mt-3">
									<p class="mb-2 text-[11px] font-semibold tracking-wide text-slate-500 uppercase">
										Related typologies
									</p>
									<div class="flex flex-wrap gap-2">
										{#each pls as pl (pl.id)}
											<span
												class="rounded-full bg-slate-100 px-2.5 py-1 text-[11px] text-slate-700"
											>
												{pl.name}
											</span>
										{/each}
									</div>
								</div>

								<div class="mt-3">
									<p class="mb-2 text-[11px] font-semibold tracking-wide text-slate-500 uppercase">
										Related techniques
									</p>
									<ul class="space-y-1 text-xs leading-5 text-slate-600">
										{#each trauma.abuse_techniques.split('\n') as value, n (n)}
											<li>• {value}</li>
										{/each}
									</ul>
								</div>
							</div>
						{/each}
					</div>
				{/if}
			</div>
		</div>
	{/if}
</div>
