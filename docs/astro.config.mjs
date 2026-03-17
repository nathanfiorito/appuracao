// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://docs.nathanfiorito.com.br',

  integrations: [
    starlight({
      title: 'Apuração Paralela',
      description:
        'Contagem paralela de votos com verificação criptográfica para eleições brasileiras.',
      defaultLocale: 'pt-BR',
      locales: {
        root: {
          label: 'Português (Brasil)',
          lang: 'pt-BR',
        },
      },
      social: [
        { icon: 'github', label: 'GitHub', href: 'https://github.com/nathanfiorito/appuracao' },
      ],
      sidebar: [
        {
          label: 'Arquitetura',
          items: [
            { label: 'Fluxo de Dados', slug: 'architecture/data-flow' },
            { label: 'Backend', slug: 'architecture/backend' },
            { label: 'Frontend', slug: 'architecture/frontend' },
            { label: 'Infraestrutura', slug: 'architecture/infrastructure' },
          ],
        },
        {
          label: 'Segurança',
          items: [{ label: 'Checklist', slug: 'security/checklist' }],
        },
        {
          label: 'Desenvolvimento',
          items: [
            { label: 'Início Rápido', slug: 'development/quickstart' },
            { label: 'Testes', slug: 'development/testing' },
          ],
        },
      ],
    }),
  ],
});
