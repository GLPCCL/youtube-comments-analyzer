export interface Comment {
    text: string;
    author: string;
    date: string;
    sentiment_score: number;
}

export interface AnalysisResults {
    positifs: Comment[];
    negatifs: Comment[];
    interrogatifs: Comment[];
    keywords: {
        [category: string]: { [keyword: string]: number };
    };
    summary: {
        [category: string]: string;
    };
}

export interface Suggestion {
    type: 'tutoriel' | 'amélioration';
    sujet: string;
    priorité: number;
}

export interface ApiResponse {
    analysis: AnalysisResults;
    visualizations: {
        distribution: any;
        keywords: { [category: string]: any };
        timeline: any;
    };
    suggestions: Suggestion[];
}
