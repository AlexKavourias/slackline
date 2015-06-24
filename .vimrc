set nu
syntax on
set ruler
set mouse=v
set expandtab                                                                                             
set shiftwidth=4                                                                                          
set softtabstop=4                                                                                         
set tabstop=8                                                                                             
let python_highlight_all=1 
set smartindent cinwords=if,elif,else,for,while,try,except,finally,def,class
set omnifunc=pythoncomplete#Complete
highlight WhitespaceEOL ctermbg=red guibg=red
