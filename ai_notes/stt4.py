# -*- coding: utf-8 -*-
import os
import time
from llama_cpp import Llama
import re


# Пример текста (замените на результат распознавания речи)
text = 'В 1914 году началась Первая мировая война, один из самых страшных кровавых и разрушительных военных конфликтов в истории человечества. А началось всё, сказалось бы, незначительных по масштабу событий, на границе серби и Австра Вендри. Правда ли, что Квайне привело убийство Франса Ферденанда? Зачем она была нужна? И чего хотели добиться противники? И можно ли было её избежать? Если вам нравится нашу видео по истории, подписывайтесь на канал и ставьте лайк под этим роликом. В начале 20-го века мир действительно стоял на пороге Большой войны. Новые империи, такие как Германия, требовали передела мира. Старые наоборот хотели сохранить своё влияние. Свои цели были и у России, уже сотню лет, стремившиеся получить контроль над Черноморскими проливами и у Италии, грязившей ославе Римской империи. Почему же война не началась раньше? На самом деле такое вполне могло произойти, Германия не однократно шла на конфликт с Франции, что грозила перерасти в Большую войну. Так в 1905-м и 1911 годах Германия разожгла два мараканских кризиса. Она спорилась в Франции контроли над стратегически важными мараканскими портами на севере Африки. В те дни все были уверены, что Германский войска вот-вот вступит во Францию. Лишь путём невероятных, дипломатических усилий, катастрофы удалось избежать. Но не надолго. 28-го июня 1914 года басниский серб Гаврилла Принцип убил наследника Австравенгерского престола Эрдс Герцога Франза Фердинанда в Сараева. Тогда в Сербии у власти стояла династия коррагеоргий вечей. Они проводили националистическую политику и стремились расширить влияние Сербии, вернуть ей былое могущество. Францфер Динант в свою очередь был сторонником расширения прав народов, живущих в Империи. Сербы видели в этом угрозу своему влиянию на балканах. По одной из версии убийства было организованно властями Сербии, дело в том, что начальник сербской разведки Драгутин Димитриевич возглавлял террористическую организацию Чёрная Рука, с которой тесно сотрудничали принципы организация молодая Босния. Но другие историки считают, что Сербия стремилась избежать возможной войны, поэтому ей было не выгодно отправлять террористов на убийство Эрдс Герцога. Смерть Сеноследника Австравен Гри привела глубочальшему дипломатическому критису. Целые месяц страны пытались найти хоть какой-то выход из ситуации, но всем становилось очевидно мирного решения не будет. Мировые войны повлияли на весь 20-ый век, расстановка сил после хакончания определила будущих экономических и политических лидеров среди стран. И они серьезно изменились по сравнению с началом столетия. Хотите разобраться, как и почему карту мира перекраивали после каждой войны. Понять, какие интересы толкают государство, воевать на чужой территории. Все это мы объясняем в нашей программе для тех, кто хочет разобраться в истории с нуля. Мы собрали для вас все самое необходимое в простой и доступной форме, ссылка в описании. К 1914 году Европа была покрыта цепочкой союзов. Германия была союзницей Австравен Гри, вместе с ними в договоре участвовал еще и Итали. Этот блок назывался «троустенным союзом», а позже он преобразовался в четверной, центральные державы. Россия, Франция и Великобритания образовали Антанту. Помимо этого Россия гарантировала свободу и независимость сербий. Австравен Гре в целом не хотела войны сервии, понимая, что за ней стоит Россия. Но саму Австравен Гре поддерживала Германия. Император Вильгельм II заверял союзников в случае любых проблем, Германия готов оказать полную военную поддержку. Фактически Германия дала Австритцем Кардбланш на развязывание войны. 23-йюля сербом выдвинули ультиматум, который требовал в кратчайшие сроки выполнить 10 пунктов. Среди них были из-за преднационалистических газет и арест причастных кубистов. Сербия согласилась выполнить все пункты, кроме одного, допустить австритских следователей на территорию страны. Это было посегательство на сербские суверенитеты независимость. А сам пункт был расписан максимально туманно, было непонятно, что именно будут делать следователи, могло дойти и до полной окупации. Опираюсь на российскую поддержку, сербы отказались выполнять ультиматум. Германия же активно довила на Австровенгрию, давала ей гарантии безопасности и подталкивала объявить войну сербий. 28-йюля это случилось. 31-йюля Россия выполняя союзнические обязательства начала мобилизацию. На самом деле Николай II пытался этого избежать. Он прекрасно понимал, к чему это приведет и не был готов брать ответственность за миллионы жизни. Но в итоге он послушал советников и подписал указ о всеобщем обилизации. Германия объявила это угрозы безопасности и потребовала прекратить подготовку войск. 1-й августа Германия объявила войну России, а 3-й августа Франции. Первая мировая война ночевалась. Германия зажатая между Францией России понимала, что затяжную войну на два фронта ей не потянуть. Поэтому был разработан план Шлиффина. Он основывался на мысли, что Россия понадобится много времени для мобилизации. Пока она будет собирать армию, Германские солдаты быстрым мощным ударом разгромят французов и выведут их из войны. А затем Россия, оставшаяся без союзников, долго не продержаться и будет разбитав кратчайшие сроки. План был надежным, как швейцарские часы, но Россия удалось провести мобилизацию намного быстрее, чем того ожидала Германия. Это спутало немцам все карты и во многом спасло францию от поражения. На западном фронте немцы нанесли огибающий удар через нейтральную белую. Они хотели разгромить французскую арню и выйти к Парижу. Но для этого немцам не хватило солдат. К тому же в битве при Марне из-за успешного наступления русских восточной пруси пришлось снять несколько дивизий на восточный фронт. В результате компании 1914 года Франция выставила, сложившийся к концу года фронт до конца войны почти никак не менялся. Началась та самая позиционная война. Сыры и холодные окопы, постоянные арт-апстрелы, самоубийственные атаки на авражеские пулеметы, все это повседневная реальность первой мировой войны, описанные в книгах Ремарка, Хемен Гуээ и десятка в других авторов. На восточном фронте ситуация складывалась иная. Российские войска успешно начавшие восточную прусскую операцию и запрощутов командования оказались разбиты в битве при Танонберге. После этого началась череда неудач, которые в итоге привели к великому отступлению 1915 года. Российская армия отошла с огромных территорий, были потерены галиция Польша Литва. На поле боя оставили множество орудий, десятки тысяч солдат погибли или попали в плен. Тем не менее полностью разгромить Россию не удалось, фронт был стабилизирован, война продолжалась. Люди осознавшие, что крышдество война явно не закончится, впадали в отчаян. В какой-то момент они даже решили на время прекратить битвы, на западном фронте начались рождественские перемирия, солдаты братались, отказывались воевать, даже играли в футбол, но это идеи продлилось недолго. В 1915 год отметился тем, что войну наконец вступило италия, но не там, где ожидалось. Итальянцы переметнулись к контанте и начали вторжение в Австера Венгрию. Итальянский фронт стал одним из самых жестоких, и в то же время без смысленных направлений войны. Первая мировая была первой войной, которая так сильно опиралась на народ. Всем было необходимо работать, не покладая ру к ради победы. Нормы и стали не регулируемый рабочий день, дефицит еды трудности с отоплением. Это продолжалось сюда самого конца войны. В 1916 году никаких изменений на западном фронте не происходило. Стороны раз за разом предпринимали самоубийственные атаки, чтобы захватить 1-2 километров выжены земли. А по геем стали битва при вердении и битва на сомне. Сумарные потери обеих сторон в каждом изражении составили почти миллион человек, но никаких изменений фронта не произошло. На восточном фронте год отметился брусиловским прорывом, наступлением российских войск, на австрийском фронте на глубину до 100 километров. Удивительная мобильность по меркам Первой мировой. От полного разгрома Австравенгрию спасли лишь подошедшие германские дивизии. Впрочем, несмотря на ошеломляющий тактический успех, никакого стратегического результата эта операция не принесла. Так ее итоги оценивал сам брусилов. Следующий 1917 год стал революционным для войны во всех смыслах. Во-первых, в России произошла февральская революция, измученный войной народ, не видящий никакого смысла и результата, поддерживал свержение Николая второго. Но временное правительство, взявшая власть в своей руки, подтвердило Антантия готовность воевать до победного конца, во многом это и предопределило его падение. Войну на стороне Антанты вступили США. Стало понятно, что Германии уже не за что не выстать. Ресурсы противника слишком великие, а в стране зимой 16-го-17 года уже начался голод из заблокады и лишений войны. Но бой не продолжалось. Уже в октябре большей вики устроили переворот в России и объявили аномерение заключить мир на любых условиях. Это решение встретило колоссальную поддержку в обществе. В марте 1918 года между советской России и центральными державами был заключен бресский мир. Но когда США прислали в Европу свежий экспедиционный корпус, стало понятно, что Германия обречена. В ноябре 1918 года в стране произошла революция. Император отрекся от престола к власти пришли социал-демократой. Новое правительство моментально заключило перемирие Сантанты, и хотя на тот момент чужие войска не входили на территорию Германии, у страны уже не было никаких ресурсов, чтобы продолжать войну. В конце концов был заключен вирсальских мир. Германия объявили главные виновниции войны. Она лишалась ряда территории, не имела права иметь армию, была обязана выплачивать внушительные репорации. Это парадило миф о невероятной жестокости вирсали. Но вряд ли можно говорить, что это было достаточно наказанием для страны, начавшей ужасную боюню в центре Европы, в ходе которой сотни городов были обращены в пыль и пострадали десятки миллионов человек. Французский маршал Фердина Андфош узнав об условиях вирсалия заявил, это не мир, это перемирие лет на 20. И он имел в виду именно мягкость договора. К сожалению, он оказался прав, память об ужасах войны не предотвратива будущих трагедий. Чтобы разобраться в настоящем, надо изучать прошлое. Для этого не обязательно читать скушные учебники, ведь есть наша программа для тех, кто хочет изучать историю с нуля. Мы открыли бесплатный доступ ко всем нашим 250 курсом на неделю. Оформляйте подписку по ссылке в описании видео и сразу отменяйте, чтобы не платить. Деньги не спишутся, а вы целую неделю сможете смотреть любые курсы. Но если вам понравится, вы можете поддержать нашу работу и оставить подписку. После пробного периода она будет стоить всего 299 рублей.         '

print("Распознанный текст:", text)



# Разделение текста на части, если он слишком длинный
def split_text(text, max_length=600):
    # Разделяем текст на предложения
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        # Проверяем длину текущего куска и добавляем предложение
        if len(current_chunk) + len(sentence) + 1 <= max_length:
            if current_chunk:
                current_chunk += " "  # Добавляем пробел между предложениями
            current_chunk += sentence
        else:
            # Если текущий кусок превышает длину, сохраняем его и начинаем новый
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = sentence

    # Добавляем последний кусок, если он не пустой
    if current_chunk:
        chunks.append(current_chunk)

    return chunks

# Загрузка модели saiga
llama_model = Llama(model_path="model-q4_K.gguf", n_gpu_layers=-1,
                    use_gpu=True)

# Функция для обработки текста через модель Llama
def process_text_with_llama(text, task):
    prompt = f"Ты языковая модель для обработки текста. В твоём ответе должен быть только обработанный текст и ничто больше. {task}: {text}"
    response = llama_model(prompt)

    if response is None or "error" in response:
        print("Ошибка при обработке текста.")
        return False  # Возвращаем False при ошибке
    print(response['choices'][0]['text'])
    return response['choices'][0]['text'].strip()





# Определение темы
chunks = split_text(text)
print(chunks)
topic = process_text_with_llama(chunks[0], "Определи тему этой лекции. В ответе напиши только тему")
print('тема:',topic)

# Создание конспекта
summary = ""
for chunk in chunks:
    success = False
    while not success:
        processed_text = process_text_with_llama(chunk, f'Перепиши текст, сократив его, оставь только самое главное. Учти, что в тексте есть лишние фразы, не касающиеся основной темы ("{topic}"), их вставлять в текст не нужно.')
        if processed_text is False:
            print("Повторный запрос для части текста...")

            continue  # Попробуем снова
        summary += processed_text + " "
        success = True  # Успех, выходим из цикла

print("готовый Конспект:", summary)
