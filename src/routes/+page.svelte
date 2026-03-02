<script lang="ts">
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';
	import FormItem from '$lib/components/FormItem.svelte';
	import { Button } from '$lib/components/ui/button/index.js';
	import * as Card from '$lib/components/ui/card/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Label } from '$lib/components/ui/label/index.js';
	import { handleError } from '$lib/consts';
	import { setApiKey } from '$lib/data.remote';

	let btnDisabled = $state(false);

	let key = $state('');

	async function localSetApiKey() {
		try {
			btnDisabled = true;
			await setApiKey(key);
			await goto(resolve('/app'));
		} catch (err) {
			handleError(err);
		} finally {
			btnDisabled = false;
		}
	}
</script>

<div
	class="flex h-full w-full items-center justify-center bg-linear-to-b from-white to-slate-50 px-4"
>
	<div class="relative w-full max-w-sm">
		<div
			class="absolute -inset-px rounded-3xl bg-linear-to-r from-pink-400 via-purple-400 to-blue-400 opacity-80 blur-[2px]"
		></div>

		<Card.Root
			class="relative rounded-3xl border border-slate-200/60 bg-white/80 shadow-xl backdrop-blur"
		>
			<Card.Header>
				<div class="flex items-center justify-between">
					<div class="flex items-center gap-3">
						<img src="/logo.jpg" alt="Logo" class="h-10 w-10 rounded-xl object-cover" />
						<div>
							<Card.Title class="text-slate-900">Login with API Key</Card.Title>
							<Card.Description class="text-slate-500">Use your OpenAI API key</Card.Description>
						</div>
					</div>

					<Button
						target="_blank"
						href="https://platform.openai.com/api-keys"
						variant="link"
						class="text-pink-500 hover:text-pink-600"
					>
						Need a key?
					</Button>
				</div>
			</Card.Header>

			<Card.Content>
				<FormItem>
					<Label>API Key</Label>
					<Input type="text" placeholder="sk-..." bind:value={key} autocomplete="off" />
				</FormItem>
			</Card.Content>

			<Card.Footer class="flex-col gap-2">
				<Button
					disabled={btnDisabled || !key.startsWith('sk-')}
					onclick={localSetApiKey}
					class="w-full bg-linear-to-r from-pink-500 via-purple-500 to-blue-500 text-white hover:opacity-95"
				>
					Login
				</Button>
			</Card.Footer>
		</Card.Root>
	</div>
</div>
