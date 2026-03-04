<script lang="ts">
	import { Button } from '$lib/components/ui/button/index.js';
	import {
		ChatBubble,
		ChatBubbleAvatar,
		ChatBubbleMessage
	} from '$lib/components/ui/chat/chat-bubble/index.js';
	import { ChatInput, ChatMessageList } from '$lib/components/ui/chat/index.js';

	const messages: {
		id: number;
		variant: 'sent' | 'received';
		avatar: string;
		message: string | null;
		isLoading?: boolean;
	}[] = [
		{
			id: 1,
			variant: 'sent',
			avatar: 'Me',
			message: 'Hello, how has your day been? I hope you are doing well.'
		},
		{
			id: 2,
			variant: 'received',
			avatar: 'AI',
			message: 'Hi, I am doing well, thank you for asking. How can I help you today?'
		},
		{
			id: 3,
			variant: 'sent',
			avatar: 'Me',
			message: 'Did you by chance have a look at the chat component?'
		},
		{
			id: 4,
			variant: 'received',
			avatar: 'AI',
			message: "No I didn't. But will check when I have time"
		},
		{ id: 5, variant: 'sent', avatar: 'Me', message: null, isLoading: true }
	];

	let currentMessage = $state('');
</script>

<ChatMessageList>
	{#each messages as message (message.id)}
		<ChatBubble variant={message.variant}>
			<ChatBubbleAvatar fallback={message.avatar} />
			<ChatBubbleMessage variant={message.variant} isLoading={message.isLoading || false}>
				{message.message}
			</ChatBubbleMessage>
		</ChatBubble>
	{/each}
</ChatMessageList>

<div class="flex gap-4">
	<ChatInput bind:value={currentMessage} />
	<Button class="mt-auto ">Send</Button>
</div>
