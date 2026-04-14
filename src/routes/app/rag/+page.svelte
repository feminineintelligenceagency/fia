<script lang="ts">
	import { Badge } from '$lib/components/ui/badge/index.js';
	import { Button } from '$lib/components/ui/button/index.js';
	import * as Card from '$lib/components/ui/card/index.js';
	import * as InputGroup from '$lib/components/ui/input-group/index.js';
	import { Separator } from '$lib/components/ui/separator/index.js';
	import { Spinner } from '$lib/components/ui/spinner/index.js';
	import type {
		AnalyzeResponse,
		PatternExplanation,
		PatternComparison,
		SafetyPlan,
		SearchResponse
	} from '$lib/types/rag.js';
	import AlertTriangle from '@lucide/svelte/icons/triangle-alert';
	import ArrowUpIcon from '@lucide/svelte/icons/arrow-up';
	import Brain from '@lucide/svelte/icons/brain';
	import CheckCircle2 from '@lucide/svelte/icons/check-circle-2';
	import ClipboardList from '@lucide/svelte/icons/clipboard-list';
	import GitCompareArrows from '@lucide/svelte/icons/git-compare-arrows';
	import HeartHandshake from '@lucide/svelte/icons/heart-handshake';
	import Info from '@lucide/svelte/icons/info';
	import Search from '@lucide/svelte/icons/search';
	import Shield from '@lucide/svelte/icons/shield';
	import ShieldAlert from '@lucide/svelte/icons/shield-alert';
	import Sparkles from '@lucide/svelte/icons/sparkles';
	import { toast } from 'svelte-sonner';

	let { data } = $props();

	// --- Analysis state ---
	let query = $state('');
	let isAnalyzing = $state(false);
	let analysisResult = $state<AnalyzeResponse | null>(null);

	// --- Explain state ---
	let selectedPattern = $state<string | null>(null);
	let patternExplanation = $state<PatternExplanation | null>(null);
	let isExplaining = $state(false);

	// --- Safety plan state ---
	let safetyPlan = $state<SafetyPlan | null>(null);
	let isGeneratingPlan = $state(false);

	// --- Compare state ---
	let compareA = $state('');
	let compareB = $state('');
	let comparison = $state<PatternComparison | null>(null);
	let isComparing = $state(false);

	// --- Search state ---
	let searchQuery = $state('');
	let searchResults = $state<SearchResponse | null>(null);
	let isSearching = $state(false);

	// --- Red Flag Self-Assessment state ---
	const redFlagCategories: {
		name: string;
		headingClass: string;
		checkedClass: string;
		boxClass: string;
		items: string[];
	}[] = [
		{
			name: 'Emotional',
			headingClass: 'text-pink-500',
			checkedClass:
				'border-pink-400 bg-pink-50 text-foreground dark:bg-pink-950/30',
			boxClass: 'border-pink-500 bg-pink-500 text-white',
			items: [
				'Belittles or mocks me in front of others',
				'Gives me the silent treatment as punishment',
				'Tells me I am overreacting when I express hurt',
				'Makes me feel guilty for having my own feelings'
			]
		},
		{
			name: 'Control',
			headingClass: 'text-purple-500',
			checkedClass:
				'border-purple-400 bg-purple-50 text-foreground dark:bg-purple-950/30',
			boxClass: 'border-purple-500 bg-purple-500 text-white',
			items: [
				'Tracks my phone, messages, or location',
				'Controls the money or how I spend it',
				'Decides who I am allowed to see or talk to',
				'Blows up when I set boundaries'
			]
		},
		{
			name: 'Isolation',
			headingClass: 'text-blue-500',
			checkedClass:
				'border-blue-400 bg-blue-50 text-foreground dark:bg-blue-950/30',
			boxClass: 'border-blue-500 bg-blue-500 text-white',
			items: [
				'Has pushed me away from close friends',
				'Discourages me from seeing my family',
				'Makes me feel like no one else understands them like I do',
				'I feel alone even when I am with them'
			]
		},
		{
			name: 'Deception',
			headingClass: 'text-amber-500',
			checkedClass:
				'border-amber-400 bg-amber-50 text-foreground dark:bg-amber-950/30',
			boxClass: 'border-amber-500 bg-amber-500 text-white',
			items: [
				'I have caught them in repeated lies',
				'Hides accounts, purchases, or whereabouts',
				'Love-bombs me, then turns cold without warning',
				'Rewrites history about things I know happened'
			]
		}
	];
	let checkedItems = $state<Set<string>>(new Set());
	let assessmentResult = $state<AnalyzeResponse | null>(null);
	let isAssessing = $state(false);
	const checkedCount = $derived(checkedItems.size);
	const riskLevel = $derived(deriveRiskLevel(checkedCount, assessmentResult));

	function toggleCheck(item: string) {
		const next = new Set(checkedItems);
		if (next.has(item)) next.delete(item);
		else next.add(item);
		checkedItems = next;
	}

	function deriveRiskLevel(
		count: number,
		result: AnalyzeResponse | null
	): {
		label: string;
		description: string;
		bannerClass: string;
		iconClass: string;
		labelClass: string;
	} {
		const hasDanger = result?.findings?.some((f) => f.type === 'danger') ?? false;
		if (count === 0)
			return {
				label: 'Not assessed',
				description: 'Check items to begin',
				bannerClass:
					'border-slate-300/50 bg-slate-50/60 dark:border-slate-500/30 dark:bg-slate-900/40',
				iconClass: 'text-slate-500',
				labelClass: 'text-slate-600 dark:text-slate-400'
			};
		if (hasDanger || count >= 10)
			return {
				label: 'Critical',
				description: 'Multiple severe red flags present',
				bannerClass: 'border-red-300/50 bg-red-50/60 dark:border-red-500/30 dark:bg-red-950/20',
				iconClass: 'text-red-500',
				labelClass: 'text-red-600 dark:text-red-400'
			};
		if (count >= 6)
			return {
				label: 'High',
				description: 'Significant pattern of concern',
				bannerClass:
					'border-orange-300/50 bg-orange-50/60 dark:border-orange-500/30 dark:bg-orange-950/20',
				iconClass: 'text-orange-500',
				labelClass: 'text-orange-600 dark:text-orange-400'
			};
		if (count >= 3)
			return {
				label: 'Moderate',
				description: 'Early warning signs present',
				bannerClass:
					'border-amber-300/50 bg-amber-50/60 dark:border-amber-500/30 dark:bg-amber-950/20',
				iconClass: 'text-amber-500',
				labelClass: 'text-amber-600 dark:text-amber-400'
			};
		return {
			label: 'Low',
			description: 'Limited red flags detected',
			bannerClass:
				'border-emerald-300/50 bg-emerald-50/60 dark:border-emerald-500/30 dark:bg-emerald-950/20',
			iconClass: 'text-emerald-500',
			labelClass: 'text-emerald-600 dark:text-emerald-400'
		};
	}

	async function handleAssess() {
		if (checkedItems.size === 0 || isAssessing) return;
		isAssessing = true;
		assessmentResult = null;
		const items = Array.from(checkedItems);
		const story =
			"I have experienced the following behaviors in my relationship: " +
			items.map((i) => `- ${i}`).join('; ') +
			'. Please analyze the manipulation patterns at play.';
		try {
			const res = await fetch('/api/rag/analyze', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ content: story })
			});
			if (!res.ok) {
				toast.error('Assessment failed');
				isAssessing = false;
				return;
			}
			assessmentResult = await res.json();
			toast.success('Assessment complete');
		} catch {
			toast.error('Failed to connect to analysis service');
		}
		isAssessing = false;
	}

	function resetAssessment() {
		checkedItems = new Set();
		assessmentResult = null;
	}

	const suggestions = [
		"He always says I'm overreacting when I bring up concerns...",
		'She isolated me from my friends and checks my phone constantly...',
		"One day he's loving, the next he gives me the silent treatment...",
		'He controls all the money and I have to ask permission to spend...',
		'She uses guilt to make me feel bad every time I set a boundary...'
	];

	const typologyNames = $derived(data.typologies.map((t) => t.name).filter(Boolean));

	async function handleAnalyze() {
		if (!query.trim() || isAnalyzing) return;
		isAnalyzing = true;
		analysisResult = null;
		selectedPattern = null;
		patternExplanation = null;
		safetyPlan = null;

		try {
			const res = await fetch('/api/rag/analyze', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ content: query })
			});
			if (!res.ok) {
				toast.error('Analysis failed');
				isAnalyzing = false;
				return;
			}
			analysisResult = await res.json();
			toast.success('Analysis complete');
		} catch {
			toast.error('Failed to connect to analysis service');
		}
		isAnalyzing = false;
	}

	async function handleExplainPattern(patternName: string) {
		if (isExplaining) return;
		if (selectedPattern === patternName && patternExplanation) {
			selectedPattern = null;
			patternExplanation = null;
			return;
		}
		selectedPattern = patternName;
		isExplaining = true;
		patternExplanation = null;
		try {
			const res = await fetch('/api/rag/explain', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ patternName })
			});
			if (!res.ok) {
				toast.error('Failed to explain pattern');
				selectedPattern = null;
				isExplaining = false;
				return;
			}
			patternExplanation = await res.json();
		} catch {
			toast.error('Failed to connect to analysis service');
			selectedPattern = null;
		}
		isExplaining = false;
	}

	async function handleSafetyPlan() {
		if (!analysisResult || isGeneratingPlan) return;
		isGeneratingPlan = true;
		safetyPlan = null;
		try {
			const res = await fetch('/api/rag/safety-plan', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					story: query,
					patternsDetected: analysisResult.patterns_detected
				})
			});
			if (!res.ok) {
				toast.error('Failed to generate safety plan');
				isGeneratingPlan = false;
				return;
			}
			safetyPlan = await res.json();
			toast.success('Safety plan generated');
		} catch {
			toast.error('Failed to connect to analysis service');
		}
		isGeneratingPlan = false;
	}

	async function handleCompare() {
		if (!compareA || !compareB || compareA === compareB || isComparing) return;
		isComparing = true;
		comparison = null;
		try {
			const res = await fetch('/api/rag/compare', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ patternA: compareA, patternB: compareB })
			});
			if (!res.ok) {
				toast.error('Failed to compare patterns');
				isComparing = false;
				return;
			}
			comparison = await res.json();
			toast.success('Comparison complete');
		} catch {
			toast.error('Failed to connect to analysis service');
		}
		isComparing = false;
	}

	async function handleSearch() {
		if (!searchQuery.trim() || isSearching) return;
		isSearching = true;
		searchResults = null;
		try {
			const res = await fetch('/api/rag/search', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ query: searchQuery, k: 8 })
			});
			if (!res.ok) {
				toast.error('Search failed');
				isSearching = false;
				return;
			}
			searchResults = await res.json();
		} catch {
			toast.error('Failed to connect to analysis service');
		}
		isSearching = false;
	}

	function severityIcon(type: string) {
		if (type === 'danger') return ShieldAlert;
		if (type === 'warning') return AlertTriangle;
		return Info;
	}

	function severityColor(type: string) {
		if (type === 'danger') return 'border-l-red-500';
		if (type === 'warning') return 'border-l-amber-500';
		return 'border-l-blue-500';
	}

	function severityTextColor(type: string) {
		if (type === 'danger') return 'text-red-500';
		if (type === 'warning') return 'text-amber-500';
		return 'text-blue-500';
	}
</script>

<!-- Background decoration -->
<div class="pointer-events-none fixed inset-0 -z-10 overflow-hidden opacity-30">
	<div
		class="absolute -top-40 -right-40 h-96 w-96 rounded-full bg-linear-to-br from-pink-400/40 to-purple-500/40 blur-3xl"
	></div>
	<div
		class="absolute -bottom-40 -left-40 h-96 w-96 rounded-full bg-linear-to-tr from-blue-400/40 to-cyan-500/40 blur-3xl"
	></div>
</div>

<div class="relative mx-auto w-full max-w-5xl px-4 py-6">
	<!-- Backend warning banner -->
	{#if !data.backendAvailable}
		<div
			class="mb-6 flex items-center gap-3 rounded-2xl border border-amber-300/50 bg-amber-50 px-5 py-4 shadow-sm dark:border-amber-500/30 dark:bg-amber-950/30"
		>
			<AlertTriangle class="h-5 w-5 shrink-0 text-amber-500" />
			<div>
				<p class="text-sm font-medium text-amber-800 dark:text-amber-200">
					RAG backend is not available
				</p>
				<p class="text-xs text-amber-600 dark:text-amber-400">
					Start the FastAPI server: <code
						class="rounded bg-amber-100 px-1.5 py-0.5 font-mono dark:bg-amber-900/50"
						>python -m uvicorn app.main:app --reload --port 8000</code
					>
				</p>
			</div>
		</div>
	{/if}

	<!-- ═══════════════════════════════════════════ -->
	<!-- HERO: Query Input                          -->
	<!-- ═══════════════════════════════════════════ -->
	<div class="relative w-full">
		<div
			class="absolute -inset-px rounded-3xl bg-linear-to-r from-pink-400 via-purple-400 to-blue-400 opacity-80 blur-[2px]"
		></div>

		<div
			class="relative rounded-3xl border border-border/60 bg-card/80 p-8 shadow-xl backdrop-blur"
		>
			<div class="flex items-center gap-3">
				<span
					class="inline-flex items-center rounded-full bg-foreground px-3 py-1 text-xs font-medium text-background"
				>
					RAG Analysis
				</span>
				<span class="text-xs text-muted-foreground">Powered by AI + Vector Search</span>
			</div>

			<h1 class="mt-4 text-4xl leading-tight font-extrabold text-foreground">
				Analyze relationship patterns<br />
				with AI.
			</h1>

			<p class="mt-3 max-w-2xl text-sm leading-relaxed text-muted-foreground">
				Describe a relationship situation. The AI will search our knowledge base and identify
				manipulation patterns, red flags, and provide supportive guidance.
			</p>

			<Separator class="my-6" />

			<InputGroup.Root
				class="rounded-2xl border border-border bg-background focus-within:border-border focus-within:[box-shadow:0_0_0_4px_rgba(236,72,153,0.12),0_0_0_8px_rgba(59,130,246,0.10)]"
			>
				<textarea
					bind:value={query}
					placeholder="Describe what you're experiencing..."
					rows="3"
					class="w-full resize-none border-none bg-transparent px-4 py-4 text-base text-foreground placeholder:text-muted-foreground focus:outline-none"
					disabled={!data.backendAvailable || isAnalyzing}
				></textarea>

				<InputGroup.Addon align="block-end">
					<InputGroup.Button
						variant="default"
						class="mr-2 mb-2 ml-auto cursor-pointer rounded-full bg-linear-to-r
						from-pink-500 via-purple-500 to-blue-500 p-3
						text-white shadow-md shadow-pink-500/20 transition hover:opacity-95 active:scale-[0.98]"
						size="icon-xs"
						onclick={handleAnalyze}
						disabled={!data.backendAvailable || isAnalyzing || !query.trim()}
					>
						{#if isAnalyzing}
							<Spinner class="h-4 w-4" />
						{:else}
							<ArrowUpIcon />
						{/if}
						<span class="sr-only">Analyze</span>
					</InputGroup.Button>
				</InputGroup.Addon>
			</InputGroup.Root>

			<div class="mt-4 flex flex-wrap gap-2">
				{#each suggestions as s (s)}
					<button
						type="button"
						class="rounded-full border border-border bg-background px-3 py-1.5 text-xs text-foreground transition hover:bg-muted"
						disabled={!data.backendAvailable || isAnalyzing}
						onclick={() => {
							query = s;
						}}
					>
						{s.length > 50 ? s.slice(0, 50) + '...' : s}
					</button>
				{/each}
			</div>

			{#if isAnalyzing}
				<div class="mt-4 flex items-center gap-2 text-sm text-muted-foreground">
					<span class="h-2 w-2 animate-pulse rounded-full bg-pink-500"></span>
					Analyzing with RAG pipeline...
				</div>
			{/if}
		</div>
	</div>

	<!-- ═══════════════════════════════════════════ -->
	<!-- ANALYSIS RESULTS                           -->
	<!-- ═══════════════════════════════════════════ -->
	{#if analysisResult}
		<div class="mt-8 space-y-6">
			<div class="flex items-center justify-between">
				<div class="flex items-center gap-4">
					<div
						class="flex h-12 w-12 items-center justify-center rounded-xl bg-linear-to-br from-pink-500 to-purple-600 shadow-lg shadow-pink-500/25"
					>
						<Brain class="h-6 w-6 text-white" />
					</div>
					<div>
						<h2
							class="bg-linear-to-r from-pink-400 via-purple-400 to-blue-400 bg-clip-text text-2xl font-bold text-transparent"
						>
							Analysis Results
						</h2>
						<p class="text-sm text-muted-foreground">
							{analysisResult.patterns_detected.length} pattern{analysisResult
								.patterns_detected.length !== 1
								? 's'
								: ''} detected
						</p>
					</div>
				</div>

				<!-- Safety Plan button -->
				<Button
					variant="outline"
					class="gap-2 border-emerald-300 text-emerald-600 hover:bg-emerald-50 dark:border-emerald-600 dark:text-emerald-400 dark:hover:bg-emerald-950/30"
					onclick={handleSafetyPlan}
					disabled={isGeneratingPlan}
				>
					{#if isGeneratingPlan}
						<Spinner class="h-4 w-4" />
					{:else}
						<HeartHandshake class="h-4 w-4" />
					{/if}
					Generate Safety Plan
				</Button>
			</div>

			<!-- Detected patterns badges -->
			{#if analysisResult.patterns_detected.length > 0}
				<div
					class="flex flex-wrap gap-2"
					style="animation: fadeInUp 0.4s ease-out 0.1s both;"
				>
					{#each analysisResult.patterns_detected as pattern (pattern)}
						<button
							type="button"
							onclick={() => handleExplainPattern(pattern)}
							class="inline-flex items-center gap-1.5 rounded-full border px-3 py-1.5 text-sm font-medium transition
								{selectedPattern === pattern
								? 'border-pink-500 bg-pink-50 text-pink-700 dark:bg-pink-950/30 dark:text-pink-300'
								: 'border-pink-300/50 bg-pink-50/50 text-pink-600 hover:border-pink-400 hover:bg-pink-50 dark:bg-pink-950/20 dark:text-pink-400 dark:hover:bg-pink-950/30'}"
						>
							<Sparkles class="h-3.5 w-3.5" />
							{pattern}
						</button>
					{/each}
				</div>
			{/if}

			<!-- Pattern explanation panel -->
			{#if selectedPattern}
				<div
					class="rounded-2xl border border-purple-200/60 bg-purple-50/50 p-6 backdrop-blur-sm dark:border-purple-500/30 dark:bg-purple-950/20"
					style="animation: fadeInUp 0.3s ease-out both;"
				>
					{#if isExplaining}
						<div class="flex items-center gap-3 text-sm text-purple-600 dark:text-purple-400">
							<Spinner class="h-4 w-4" />
							Getting AI explanation for "{selectedPattern}"...
						</div>
					{:else if patternExplanation}
						<h3 class="mb-3 text-lg font-semibold text-purple-900 dark:text-purple-200">
							{patternExplanation.pattern_name}
						</h3>
						<p class="mb-4 text-sm leading-relaxed text-purple-800 dark:text-purple-300">
							{patternExplanation.explanation}
						</p>

						{#if patternExplanation.key_red_flags.length > 0}
							<div class="mb-4">
								<h4 class="mb-2 text-xs font-semibold tracking-wide text-red-600 uppercase dark:text-red-400">
									Red Flags
								</h4>
								<div class="flex flex-wrap gap-2">
									{#each patternExplanation.key_red_flags as flag (flag)}
										<Badge variant="destructive" class="bg-red-100 text-red-700 hover:bg-red-100 dark:bg-red-950/50 dark:text-red-300">
											{flag}
										</Badge>
									{/each}
								</div>
							</div>
						{/if}

						{#if patternExplanation.safety_tips.length > 0}
							<div>
								<h4 class="mb-2 text-xs font-semibold tracking-wide text-emerald-600 uppercase dark:text-emerald-400">
									Safety Tips
								</h4>
								<ul class="space-y-1.5">
									{#each patternExplanation.safety_tips as tip (tip)}
										<li class="flex items-start gap-2 text-sm text-emerald-800 dark:text-emerald-300">
											<Shield class="mt-0.5 h-4 w-4 shrink-0 text-emerald-500" />
											{tip}
										</li>
									{/each}
								</ul>
							</div>
						{/if}
					{/if}
				</div>
			{/if}

			<!-- Safety Plan -->
			{#if safetyPlan}
				<Card.Root
					class="overflow-hidden border-emerald-300/50 bg-emerald-50/50 backdrop-blur-sm dark:border-emerald-600/30 dark:bg-emerald-950/20"
					style="animation: fadeInUp 0.4s ease-out both;"
				>
					<Card.Header>
						<div class="flex items-center gap-3">
							<HeartHandshake class="h-5 w-5 text-emerald-600 dark:text-emerald-400" />
							<Card.Title class="text-lg text-emerald-900 dark:text-emerald-200">Safety Plan</Card.Title>
						</div>
					</Card.Header>
					<Card.Content class="space-y-5">
						<p class="text-sm leading-relaxed italic text-emerald-700 dark:text-emerald-300">
							"{safetyPlan.affirmation}"
						</p>

						<div>
							<h4 class="mb-2 text-xs font-semibold tracking-wide text-emerald-700 uppercase dark:text-emerald-400">
								Immediate Steps
							</h4>
							<ul class="space-y-1.5">
								{#each safetyPlan.immediate_steps as step (step)}
									<li class="flex items-start gap-2 text-sm text-foreground">
										<span class="mt-1 h-1.5 w-1.5 shrink-0 rounded-full bg-emerald-500"></span>
										{step}
									</li>
								{/each}
							</ul>
						</div>

						<div>
							<h4 class="mb-2 text-xs font-semibold tracking-wide text-emerald-700 uppercase dark:text-emerald-400">
								Long-Term Strategies
							</h4>
							<ul class="space-y-1.5">
								{#each safetyPlan.long_term_strategies as strategy (strategy)}
									<li class="flex items-start gap-2 text-sm text-foreground">
										<span class="mt-1 h-1.5 w-1.5 shrink-0 rounded-full bg-blue-500"></span>
										{strategy}
									</li>
								{/each}
							</ul>
						</div>

						<div>
							<h4 class="mb-2 text-xs font-semibold tracking-wide text-emerald-700 uppercase dark:text-emerald-400">
								Resources
							</h4>
							<ul class="space-y-1.5">
								{#each safetyPlan.resources as resource (resource)}
									<li class="flex items-start gap-2 text-sm text-foreground">
										<Shield class="mt-0.5 h-4 w-4 shrink-0 text-emerald-500" />
										{resource}
									</li>
								{/each}
							</ul>
						</div>
					</Card.Content>
				</Card.Root>
			{/if}

			<!-- AI response content -->
			<Card.Root
				class="overflow-hidden border-muted/50 bg-card/80 backdrop-blur-sm"
				style="animation: fadeInUp 0.4s ease-out 0.15s both;"
			>
				<Card.Header>
					<Card.Title class="text-lg">AI Analysis</Card.Title>
				</Card.Header>
				<Card.Content>
					<p class="whitespace-pre-wrap text-sm leading-relaxed text-muted-foreground">
						{analysisResult.content}
					</p>
				</Card.Content>
			</Card.Root>

			<!-- Findings -->
			{#if analysisResult.findings.length > 0}
				<div class="space-y-3">
					<h3 class="text-sm font-semibold text-foreground">
						Findings ({analysisResult.findings.length})
					</h3>

					{#each analysisResult.findings as finding, i (finding.title + i)}
						{@const Icon = severityIcon(finding.type)}
						<div
							class="rounded-xl border border-muted/50 border-l-4 bg-card/80 p-4 backdrop-blur-sm {severityColor(finding.type)}"
							style="animation: fadeInUp 0.4s ease-out {0.2 + i * 0.05}s both;"
						>
							<div class="flex items-start gap-3">
								<Icon class="mt-0.5 h-5 w-5 shrink-0 {severityTextColor(finding.type)}" />
								<div>
									<div class="flex items-center gap-2">
										<p class="text-sm font-semibold text-foreground">{finding.title}</p>
										<Badge
											variant="outline"
											class="text-xs uppercase {severityTextColor(finding.type)} border-current/30"
										>
											{finding.type}
										</Badge>
									</div>
									<p class="mt-1 text-sm text-muted-foreground">{finding.description}</p>
									{#if finding.matched_pattern}
										<button
											type="button"
											class="mt-2 text-xs font-medium text-pink-500 hover:text-pink-600"
											onclick={() => finding.matched_pattern && handleExplainPattern(finding.matched_pattern)}
										>
											Learn about "{finding.matched_pattern}" →
										</button>
									{/if}
								</div>
							</div>
						</div>
					{/each}
				</div>
			{/if}
		</div>
	{/if}

	<!-- ═══════════════════════════════════════════ -->
	<!-- SEMANTIC SEARCH                            -->
	<!-- ═══════════════════════════════════════════ -->
	<Separator class="my-10" />

	<div class="mb-6 flex items-center gap-4">
		<div
			class="flex h-12 w-12 items-center justify-center rounded-xl bg-linear-to-br from-cyan-500 to-blue-600 shadow-lg shadow-blue-500/25"
		>
			<Search class="h-6 w-6 text-white" />
		</div>
		<div>
			<h2
				class="bg-linear-to-r from-cyan-400 via-blue-400 to-purple-400 bg-clip-text text-2xl font-bold text-transparent"
			>
				Semantic Search
			</h2>
			<p class="text-sm text-muted-foreground">Search the knowledge base by meaning</p>
		</div>
	</div>

	<div class="flex gap-3">
		<input
			type="text"
			bind:value={searchQuery}
			placeholder="e.g. gaslighting tactics, love bombing signs..."
			class="flex-1 rounded-xl border border-border bg-background px-4 py-3 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-pink-500/20"
			disabled={!data.backendAvailable || isSearching}
			onkeydown={(e) => e.key === 'Enter' && handleSearch()}
		/>
		<Button
			class="rounded-xl bg-linear-to-r from-cyan-500 to-blue-500 text-white hover:opacity-95"
			onclick={handleSearch}
			disabled={!data.backendAvailable || isSearching || !searchQuery.trim()}
		>
			{#if isSearching}
				<Spinner class="h-4 w-4" />
			{:else}
				<Search class="h-4 w-4" />
			{/if}
			Search
		</Button>
	</div>

	{#if searchResults}
		<div class="mt-4 space-y-3">
			<p class="text-xs text-muted-foreground">{searchResults.count} results for "{searchResults.query}"</p>
			{#each searchResults.results as result, i (result.content.slice(0, 40) + i)}
				<div
					class="rounded-xl border border-muted/50 bg-card/80 p-4 backdrop-blur-sm"
					style="animation: fadeInUp 0.3s ease-out {i * 0.04}s both;"
				>
					<div class="mb-2 flex items-center justify-between">
						<Badge variant="secondary" class="text-xs">
							{result.metadata?.player_type ?? result.metadata?.category ?? 'Pattern'}
						</Badge>
						<span class="text-xs text-muted-foreground">
							{(result.relevance_score * 100).toFixed(0)}% match
						</span>
					</div>
					<p class="text-sm leading-relaxed text-foreground">{result.content}</p>
				</div>
			{/each}
		</div>
	{/if}

	<!-- ═══════════════════════════════════════════ -->
	<!-- PATTERN COMPARISON                         -->
	<!-- ═══════════════════════════════════════════ -->
	{#if typologyNames.length >= 2}
		<Separator class="my-10" />

		<div class="mb-6 flex items-center gap-4">
			<div
				class="flex h-12 w-12 items-center justify-center rounded-xl bg-linear-to-br from-amber-500 to-orange-600 shadow-lg shadow-amber-500/25"
			>
				<GitCompareArrows class="h-6 w-6 text-white" />
			</div>
			<div>
				<h2
					class="bg-linear-to-r from-amber-400 via-orange-400 to-red-400 bg-clip-text text-2xl font-bold text-transparent"
				>
					Compare Patterns
				</h2>
				<p class="text-sm text-muted-foreground">
					See how two manipulation patterns differ
				</p>
			</div>
		</div>

		<div class="flex flex-col gap-3 sm:flex-row sm:items-end">
			<div class="flex-1">
				<label for="compare-a" class="mb-1 block text-xs font-medium text-muted-foreground">Pattern A</label>
				<select
					id="compare-a"
					bind:value={compareA}
					class="w-full rounded-xl border border-border bg-background px-4 py-3 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-pink-500/20"
				>
					<option value="">Select a pattern...</option>
					{#each typologyNames as name (name)}
						<option value={name} disabled={name === compareB}>{name}</option>
					{/each}
				</select>
			</div>
			<span class="hidden text-muted-foreground sm:block">vs</span>
			<div class="flex-1">
				<label for="compare-b" class="mb-1 block text-xs font-medium text-muted-foreground">Pattern B</label>
				<select
					id="compare-b"
					bind:value={compareB}
					class="w-full rounded-xl border border-border bg-background px-4 py-3 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-pink-500/20"
				>
					<option value="">Select a pattern...</option>
					{#each typologyNames as name (name)}
						<option value={name} disabled={name === compareA}>{name}</option>
					{/each}
				</select>
			</div>
			<Button
				class="rounded-xl bg-linear-to-r from-amber-500 to-orange-500 text-white hover:opacity-95"
				onclick={handleCompare}
				disabled={!compareA || !compareB || compareA === compareB || isComparing || !data.backendAvailable}
			>
				{#if isComparing}
					<Spinner class="h-4 w-4" />
				{:else}
					<GitCompareArrows class="h-4 w-4" />
				{/if}
				Compare
			</Button>
		</div>

		{#if comparison}
			<div class="mt-6 grid gap-4 md:grid-cols-2" style="animation: fadeInUp 0.4s ease-out both;">
				<Card.Root class="border-emerald-300/50 bg-emerald-50/30 dark:border-emerald-600/30 dark:bg-emerald-950/20">
					<Card.Header>
						<Card.Title class="text-sm text-emerald-700 dark:text-emerald-400">Similarities</Card.Title>
					</Card.Header>
					<Card.Content>
						<ul class="space-y-2">
							{#each comparison.similarities as item (item)}
								<li class="flex items-start gap-2 text-sm text-foreground">
									<span class="mt-1 h-1.5 w-1.5 shrink-0 rounded-full bg-emerald-500"></span>
									{item}
								</li>
							{/each}
						</ul>
					</Card.Content>
				</Card.Root>

				<Card.Root class="border-orange-300/50 bg-orange-50/30 dark:border-orange-600/30 dark:bg-orange-950/20">
					<Card.Header>
						<Card.Title class="text-sm text-orange-700 dark:text-orange-400">Differences</Card.Title>
					</Card.Header>
					<Card.Content>
						<ul class="space-y-2">
							{#each comparison.differences as item (item)}
								<li class="flex items-start gap-2 text-sm text-foreground">
									<span class="mt-1 h-1.5 w-1.5 shrink-0 rounded-full bg-orange-500"></span>
									{item}
								</li>
							{/each}
						</ul>
					</Card.Content>
				</Card.Root>

				<div class="rounded-xl border border-red-300/50 bg-red-50/30 p-4 md:col-span-2 dark:border-red-600/30 dark:bg-red-950/20">
					<h4 class="mb-2 text-xs font-semibold tracking-wide text-red-600 uppercase dark:text-red-400">
						Combined Danger
					</h4>
					<p class="text-sm leading-relaxed text-foreground">{comparison.combined_danger}</p>
				</div>
			</div>
		{/if}
	{/if}

	<!-- ═══════════════════════════════════════════ -->
	<!-- RED FLAG SELF-ASSESSMENT                   -->
	<!-- ═══════════════════════════════════════════ -->
	<Separator class="my-10" />

	<div class="mb-6 flex items-center gap-4">
		<div
			class="flex h-12 w-12 items-center justify-center rounded-xl bg-linear-to-br from-rose-500 to-pink-600 shadow-lg shadow-rose-500/25"
		>
			<ClipboardList class="h-6 w-6 text-white" />
		</div>
		<div>
			<h2
				class="bg-linear-to-r from-rose-400 via-pink-400 to-purple-400 bg-clip-text text-2xl font-bold text-transparent"
			>
				Red Flag Self-Assessment
			</h2>
			<p class="text-sm text-muted-foreground">
				Check behaviors you've experienced — AI will identify the patterns at play
			</p>
		</div>
	</div>

	<div class="relative">
		<div
			class="absolute -inset-px rounded-3xl bg-linear-to-r from-rose-400 via-pink-400 to-purple-400 opacity-60 blur-[2px]"
		></div>

		<div
			class="relative rounded-3xl border border-border/60 bg-card/80 p-6 shadow-xl backdrop-blur sm:p-8"
		>
			<div class="grid gap-6 sm:grid-cols-2">
				{#each redFlagCategories as category (category.name)}
					<div>
						<h3 class="mb-3 text-xs font-semibold tracking-wider uppercase {category.headingClass}">
							{category.name}
						</h3>
						<div class="space-y-2">
							{#each category.items as item (item)}
								{@const isChecked = checkedItems.has(item)}
								<button
									type="button"
									onclick={() => toggleCheck(item)}
									disabled={isAssessing}
									class="group flex w-full items-start gap-3 rounded-xl border px-3 py-2.5 text-left text-sm transition {isChecked
										? category.checkedClass
										: 'border-border bg-background hover:border-pink-300/60 hover:bg-muted/50'}"
								>
									<span
										class="mt-0.5 flex h-4 w-4 shrink-0 items-center justify-center rounded border transition {isChecked
											? category.boxClass
											: 'border-border bg-background'}"
									>
										{#if isChecked}
											<CheckCircle2 class="h-3 w-3" />
										{/if}
									</span>
									<span class="leading-snug">{item}</span>
								</button>
							{/each}
						</div>
					</div>
				{/each}
			</div>

			<Separator class="my-6" />

			<div class="flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-center">
				<div class="flex items-center gap-3">
					<Badge
						variant="outline"
						class="border-rose-300/50 bg-rose-50 text-rose-600 dark:bg-rose-950/30 dark:text-rose-300"
					>
						{checkedCount} checked
					</Badge>
					{#if checkedCount > 0}
						<button
							type="button"
							class="text-xs text-muted-foreground underline-offset-2 hover:underline"
							onclick={resetAssessment}
						>
							Reset
						</button>
					{/if}
				</div>
				<Button
					class="rounded-full bg-linear-to-r from-rose-500 via-pink-500 to-purple-500 text-white shadow-md shadow-pink-500/20 hover:opacity-95 active:scale-[0.98]"
					onclick={handleAssess}
					disabled={!data.backendAvailable || isAssessing || checkedCount === 0}
				>
					{#if isAssessing}
						<Spinner class="h-4 w-4" />
					{:else}
						<Sparkles class="h-4 w-4" />
					{/if}
					Analyze My Checklist
				</Button>
			</div>

			{#if assessmentResult}
				<div class="mt-6 space-y-4" style="animation: fadeInUp 0.4s ease-out both;">
					<!-- Risk level banner -->
					<div class="flex items-center justify-between rounded-2xl border p-5 {riskLevel.bannerClass}">
						<div class="flex items-center gap-3">
							<ShieldAlert class="h-6 w-6 {riskLevel.iconClass}" />
							<div>
								<p class="text-xs font-semibold tracking-wider uppercase {riskLevel.labelClass}">
									Risk Level
								</p>
								<p class="text-lg font-bold text-foreground">{riskLevel.label}</p>
							</div>
						</div>
						<p class="hidden text-sm text-muted-foreground sm:block">{riskLevel.description}</p>
					</div>

					<!-- Matched patterns -->
					{#if assessmentResult.patterns_detected.length > 0}
						<div>
							<h4 class="mb-2 text-xs font-semibold tracking-wide text-muted-foreground uppercase">
								Matched patterns
							</h4>
							<div class="flex flex-wrap gap-2">
								{#each assessmentResult.patterns_detected as pattern (pattern)}
									<button
										type="button"
										onclick={() => handleExplainPattern(pattern)}
										class="inline-flex items-center gap-1.5 rounded-full border border-pink-300/50 bg-pink-50/50 px-3 py-1.5 text-sm font-medium text-pink-600 transition hover:border-pink-400 hover:bg-pink-50 dark:bg-pink-950/20 dark:text-pink-400 dark:hover:bg-pink-950/30"
									>
										<Sparkles class="h-3.5 w-3.5" />
										{pattern}
									</button>
								{/each}
							</div>
						</div>
					{/if}

					<!-- AI summary -->
					<Card.Root class="border-muted/50 bg-card/80 backdrop-blur-sm">
						<Card.Header>
							<Card.Title class="text-sm">AI Summary</Card.Title>
						</Card.Header>
						<Card.Content>
							<p class="whitespace-pre-wrap text-sm leading-relaxed text-muted-foreground">
								{assessmentResult.content}
							</p>
						</Card.Content>
					</Card.Root>
				</div>
			{/if}
		</div>
	</div>
</div>

<style>
	@keyframes fadeInUp {
		from {
			opacity: 0;
			transform: translateY(20px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}
</style>
