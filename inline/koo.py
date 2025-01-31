# Jarvis - Userbot

from telethon.tl.types import InputWebDocument as wb
from telethon.tl.custom import Button
from . import in_pattern, InlinePlugin, async_searcher

_koo_ = {}


@in_pattern("koo", owner=True)
async def koo_search(jar):
    """Search Users on koo with API"""
    try:
        match = jar.text.split(maxsplit=1)[1].lower()
        match_ = match
    except IndexError:
        await jar.answer(
            [], switch_pm="Enter Query to Search..", switch_pm_param="start"
        )
        return
    if _koo_.get(match):
        return await jar.answer(
            _koo_[match], switch_pm="• Koo Search •", switch_pm_param="start"
        )
    res = []
    se_ = None
    key_count = None
    if " | " in match:
        match = match.split(" | ", maxsplit=1)
        try:
            key_count = int(match[1])
        except ValueError:
            pass
        match = match[0]
    match = match.replace(" ", "+")
    req = await async_searcher(
        f"https://www.kooapp.com/apiV1/search?query={match}&searchType=EXPLORE",
        re_json=True,
    )
    if key_count:
        try:
            se_ = [req["feed"][key_count - 1]]
        except KeyError:
            pass
    if not se_:
        se_ = req["feed"]
    for count, feed in enumerate(se_[:10]):
        if feed["uiItemType"] == "search_profile":
            count += 1
            item = feed["items"][0]
            profileImage = (
                item["profileImageBaseUrl"]
                if item.get("profileImageBaseUrl")
                else "https://telegra.ph/file/dc28e69bd7ea2c0f25329.jpg"
            )
            extra = await async_searcher(
                "https://www.kooapp.com/apiV1/users/handle/" + item["userHandle"],
                re_json=True,
            )
            img = wb(profileImage, 0, "image/jpeg", [])
            text = f"‣ **Name :** `{item['name']}`"
            if extra.get("title"):
                text += f"\n‣ **Title :** `{extra['title']}`"
            text += f"\n‣ **Username :** `@{item['userHandle']}`"
            if extra.get("description"):
                text += f"\n‣ **Description :** `{extra['description']}`"
            text += f"\n‣ **Followers :** `{extra['followerCount']}`    ‣ **Following :** {extra['followingCount']}"
            if extra.get("socialProfile") and extra["socialProfile"].get("website"):
                text += f"\n‣ **Website :** {extra['socialProfile']['website']}"
            res.append(
                await jar.builder.article(
                    title=item["name"],
                    description=item.get("title") or f"@{item['userHandle']}",
                    type="photo",
                    content=img,
                    thumb=img,
                    include_media=True,
                    text=text,
                    buttons=[
                        Button.url(
                            "View",
                            "https://kooapp.com/profile/" + item["userHandle"],
                        ),
                        Button.switch_inline(
                            "• Share •",
                            query=jar.text if key_count else f"{jar.text} | {count}",
                        ),
                    ],
                )
            )

    if not res:
        switch = "No Results Found :("
    else:
        _koo_.update({match_: res})
        switch = f"Showing {len(res)} Results!"
    await jar.answer(res, switch_pm=switch, switch_pm_param="start")


InlinePlugin.update({"Kᴏᴏ Sᴇᴀʀᴄʜ": "koo @__kumar__amit"})
