'use client';

import React, { useState, useEffect, useRef } from 'react';
import { toast } from 'react-toastify';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { sendChatMessage, getAgentConfig, configureAgent, AgentConfig } from '@/services/chat';

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'ai';
  timestamp: Date;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [agentConfig, setAgentConfig] = useState<AgentConfig | null>(null);
  const [configLoading, setConfigLoading] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchAgentConfig();
    
    // Add welcome message
    setMessages([
      {
        id: '1',
        content: 'Hello! How can I assist you today?',
        sender: 'ai',
        timestamp: new Date(),
      },
    ]);
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const fetchAgentConfig = async () => {
    try {
      setConfigLoading(true);
      const config = await getAgentConfig();
      setAgentConfig(config);
    } catch (error) {
      console.error('Error fetching agent config:', error);
      toast.error('Failed to fetch AI agent configuration');
      // Set default config
      setAgentConfig({
        is_active: true,
        store_level: 'user_id',
        faq_threshold: 0.75,
      });
    } finally {
      setConfigLoading(false);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!input.trim()) return;
    
    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      content: input,
      sender: 'user',
      timestamp: new Date(),
    };
    
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);
    
    try {
      // Send message to API
      const response = await sendChatMessage({ content: input });
      
      // Add AI response
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: response.message,
        sender: 'ai',
        timestamp: new Date(),
      };
      
      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      toast.error('Failed to send message');
      
      // Add error message
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: 'Sorry, I encountered an error. Please try again later.',
        sender: 'ai',
        timestamp: new Date(),
      };
      
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const toggleAgentStatus = async () => {
    if (!agentConfig) return;
    
    try {
      const updatedConfig = { ...agentConfig, is_active: !agentConfig.is_active };
      await configureAgent(updatedConfig);
      setAgentConfig(updatedConfig);
      toast.success(`AI agent ${updatedConfig.is_active ? 'enabled' : 'disabled'} successfully`);
    } catch (error) {
      console.error('Error updating agent config:', error);
      toast.error('Failed to update AI agent configuration');
    }
  };

  return (
    <DashboardLayout>
      <div className="px-4 py-6 sm:px-0">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-semibold text-gray-900">AI Chat</h1>
          {!configLoading && agentConfig && (
            <Button
              variant={agentConfig.is_active ? 'destructive' : 'default'}
              onClick={toggleAgentStatus}
            >
              {agentConfig.is_active ? 'Disable AI Agent' : 'Enable AI Agent'}
            </Button>
          )}
        </div>

        <div className="mt-6 bg-white shadow rounded-lg flex flex-col h-[calc(100vh-12rem)]">
          <div className="flex-1 p-4 overflow-y-auto">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`mb-4 flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-xs md:max-w-md lg:max-w-lg xl:max-w-xl rounded-lg px-4 py-2 ${
                    message.sender === 'user'
                      ? 'bg-blue-500 text-white'
                      : 'bg-gray-200 text-gray-800'
                  }`}
                >
                  <p className="text-sm">{message.content}</p>
                  <p className="text-xs mt-1 opacity-70">
                    {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </p>
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          <div className="border-t p-4">
            <form onSubmit={handleSendMessage} className="flex">
              <Input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Type your message..."
                disabled={loading || (agentConfig && !agentConfig.is_active)}
                className="flex-1 mr-2"
              />
              <Button type="submit" disabled={loading || !input.trim() || (agentConfig && !agentConfig.is_active)}>
                {loading ? 'Sending...' : 'Send'}
              </Button>
            </form>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
